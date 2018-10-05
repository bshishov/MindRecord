'use strict'
const path = require('path');
const utils = require('./utils');
const config = require('../config');

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}

const env = process.env.NODE_ENV === 'testing'
  ? require('../config/test.env')
  : require('../config/prod.env')

module.exports = {
  entry: './src/mindrecord.js',
  devtool: 'source-map',
  output: {
    filename: utils.assetsPath('js/mindrecord.js'),
    path: config.build.assetsRoot
  },
  resolve: {
    extensions: ['.js', '.json'],
    alias: {
      '@': resolve('src'),
    }
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [resolve('src'), resolve('test'), resolve('node_modules/webpack-dev-server/client')]
      }
    ]
  }
};
