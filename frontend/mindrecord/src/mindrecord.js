import {b64DecodeUnicode} from "./utils/utils";

const accessTokenKey = 'access_token';
const refreshTokenKey = 'access_token';

class API {
  constructor (apiPath='http://localhost:8081/api') {
    if (apiPath.endsWith('/')) {
      this.apiPath = apiPath.substring(0, apiPath.length - 1);
    } else {
      this.apiPath = apiPath
      this._user = null;
    }

    this.user;
  }

  get isAuthorized() {
    let token = localStorage.getItem(accessTokenKey);
    return token != null;
  }

  get user() {
    if(!this._user) {
      let token = localStorage.getItem(accessTokenKey);
      if (!token) {
        this.log('No auth token found')
        return null
      }

      if (!this.isValidToken(token)) {
        this.log('Invalid token in localStorage', token)
        return null
      }

      let parts = token.split('.');
      if (parts.length !== 3) {
        this.log('Invalid token in localStorage', token)
        return null
      }

      let decodedPayload = b64DecodeUnicode(parts[1]);

      this.log('User', decodedPayload);
      this._user = JSON.parse(decodedPayload);
    }
    return this._user;
  }

  loginAnonymous() {
    this.log('Anonymous authorization');
    return this.request('/auth', 'POST')
      .then(this.saveTokens.bind(this));
  }

  loginEmail(email, password) {
    this.log('Email authorization');
    let payload = new FormData();
    payload.append('email', email);
    payload.append('password', password);

    return this.request('/auth', 'POST', false, payload)
      .then(this.saveTokens.bind(this));
  }

  request(path, method='GET', auth=false, body=null, json=true) {
    let headers = {}
    if(auth) {
      let access_token = localStorage.getItem(accessTokenKey)
      if (access_token == null)
        throw Error('Unauthorized')
      headers['Authorization'] = `Bearer ${access_token}`
    }
    return fetch(`${this.apiPath}${path}`, {method, headers, body})
      .then((response) => {
        if(json)
          return response.json()
        return response.text()
      })
  }

  logout(){
    console.log('[API] Logging out')
    localStorage.removeItem(accessTokenKey);
    localStorage.removeItem(refreshTokenKey);
    this._user = null;
  }

  saveTokens(data) {
    return new Promise((success, fail) => {
      this.log('Received token-data', data);
      if (accessTokenKey in data && refreshTokenKey in data) {
        let accessToken = data[accessTokenKey];
        let refreshToken = data[refreshTokenKey];
        if(this.isValidToken(accessToken) && this.isValidToken(refreshToken)) {
          localStorage.setItem(accessTokenKey, data[accessTokenKey]);
          localStorage.setItem(refreshTokenKey, data[refreshTokenKey]);
          success(data);
          return;
        }
      }
      fail(Error('Invalid authorization data'));
    });
  }

  getWebTests(){
    return this.request('/tests');
  }

  getTest(testId){
    return this.request(`/tests/${testId}`);
  }

  getResults(resultId){
    return this.request(`/results/${resultId}`);
  }

  getResultsLog(resultId){
    return this.request(`/results/${resultId}/log`, 'GET', true, null, false);
  }

  getResultsErrorLog(resultId){
    return this.request(`/results/${resultId}/error_log`, 'GET', true, null, false);
  }

  postResults(testId, results){
    let formData = new FormData();
    for (let key in results ) {
      formData.append(key, results[key]);
    }

    return this.request(`/tests/${testId}/results`, 'POST', true, formData);
  }

  log() {
    console.log('[API]', ...arguments);
  }

  isValidToken(token) {
    if(!token)
      return false;
    let parts = token.split('.');
    return parts.length === 3;
  }
}

export {
  accessTokenKey,
  refreshTokenKey,
  API
}
