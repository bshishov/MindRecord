from bson import ObjectId
import datetime

from mindrecord.utils import HTTPError, Status
from mindrecord.app import db


__all__ = ['TestResult', 'FieldError']


class FieldError(RuntimeError):
    def __init__(self, field_name: str, message: str):
        super().__init__(message)
        self.message = message
        self.field_name = field_name

    def __str__(self):
        return 'Field [{0}]: {1}'.format(self.field_name, self.message)


class Field(object):
    value = None

    def __init__(self, dtype=None, default_value=None, db_field=None, allow_none=True):
        self.attr_name = None
        self.db_field = db_field
        self.dtype = dtype
        self.allow_none = allow_none

        self.default_value = default_value
        self._value = None
        self.is_dirty = False

    def set_default(self):
        if callable(self.default_value):
            val = self.default_value()
        else:
            val = self.default_value

        # self.validate(val)
        self._value = val

    def validate(self, value):
        if value is None:
            if not self.allow_none:
                raise FieldError(self.attr_name, 'None values are not allowed')
        else:
            if not isinstance(value, self.dtype):
                raise FieldError(self.attr_name, 'Type {0} expected, got {1}'.format(self.dtype, type(value)))

    def encode(self):
        self.validate(self.value)
        return self.value

    def decode(self, value):
        # Validation bypassed
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value


class MongoModel(object):
    collection = None
    _fields = {}

    def __init__(self, **kwargs):
        attrs = self.__class__.__dict__.copy()
        attrs.update(self.__dict__)

        # Collect fields
        for k, v in attrs.items():
            if isinstance(v, Field):
                v.attr_name = k
                if not v.db_field:
                    v.db_field = k
                self._fields[k] = v

        # Initialize fields
        for key in self._fields:
            if key in kwargs:
                self._fields[key].value = kwargs[key]
            else:
                self._fields[key].set_default()

    def save(self):
        mongo_obj = self.to_mongo()
        self.collection.update_one({'_id': mongo_obj.get('_id')}, {'$set': mongo_obj}, upsert=True)

    def to_mongo(self) -> dict:
        mongo_obj = {}
        for attr, field in self._fields.items():
            mongo_obj[field.db_field] = field.encode()
        return mongo_obj

    @classmethod
    def from_mongo(cls, mongo_obj: dict) -> object:
        obj = cls()
        for attr, field in cls._fields.items():
            if field.db_field not in mongo_obj:
                field.value = field.default_value
            else:
                field.decode(mongo_obj.get(field.db_field))
        return obj

    @classmethod
    def find_one(cls, **kwargs) -> object:
        obj = cls.collection.find_one(filter=kwargs)
        if obj is None:
            return None
        return cls.from_mongo(obj)

    @classmethod
    def get_by_id(cls, id: ObjectId) -> object:
        if isinstance(id, str):
            id = ObjectId(id)
        obj = cls.collection.find_one({'_id': id})
        if not obj:
            return None
        return cls.from_mongo(obj)

    @classmethod
    def get_by_id_or_404(cls, id: ObjectId) -> object:
        obj = cls.get_by_id(id)
        if not obj:
            raise HTTPError(Status.NOT_FOUND)
        return obj

    def __getattribute__(self, name):
        if name != '_fields' and name in self._fields:
            return self._fields[name].value
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in self._fields:
            self._fields[name].value = value
        else:
            object.__setattr__(self, name, value)


class TestResult(MongoModel):
    collection = db['results']

    id = Field(dtype=ObjectId, allow_none=False, db_field='_id', default_value=lambda: ObjectId())
    state = Field(dtype=str, allow_none=False, default_value='raw')
    created = Field(dtype=datetime.datetime, allow_none=False, default_value=datetime.datetime.utcnow)
    processed = Field(dtype=datetime.datetime, allow_none=True)
    user = Field(dtype=ObjectId, allow_none=False)
    test = Field(dtype=str, allow_none=True)
    data = Field(dtype=dict, allow_none=True)
    directory = Field(dtype=str, allow_none=False)
    raw_file = Field(dtype=str, allow_none=False)
    output_file = Field(dtype=str, allow_none=False)
