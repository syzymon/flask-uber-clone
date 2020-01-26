/*
 * Main Javascript file for flask_uber_clone.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
require('@fortawesome/fontawesome-free');
window.$ = window.jQuery = require('jquery');
require('popper.js');
require('bootstrap');

require.context(
  '../img', // context folder
  true, // include subdirectories
  /.*/, // RegExp
);

// Your own code
require('./plugins.js');
require('./script.js');
