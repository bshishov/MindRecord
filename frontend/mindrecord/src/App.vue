<template>
  <div id="app">
    <Header />
    <router-view/>
    <Footer />
  </div>
</template>

<script>
import Footer from "./components/blocks/Footer";
import Header from "./components/blocks/Header";

export default {
  name: 'App',
  components: {Header, Footer}
}
</script>

<style>
  /* http://meyerweb.com/eric/tools/css/reset/
   v2.0 | 20110126
   License: none (public domain)
  */
  html, body, div, span, applet, object, iframe,
  h1, h2, h3, h4, h5, h6, p, blockquote, pre,
  a, abbr, acronym, address, big, cite, code,
  del, dfn, em, img, ins, kbd, q, s, samp,
  small, strike, strong, sub, sup, tt, var,
  b, u, i, center,
  dl, dt, dd, ol, ul, li,
  fieldset, form, label, legend,
  table, caption, tbody, tfoot, thead, tr, th, td,
  article, aside, canvas, details, embed,
  figure, figcaption, footer, header, hgroup,
  menu, nav, output, ruby, section, summary,
  time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
  }
  /* HTML5 display-role reset for older browsers */
  article, aside, details, figcaption, figure,
  footer, header, hgroup, menu, nav, section {
    display: block;
  }
  body {
    line-height: 1;
  }
  ol, ul {
    list-style: none;
  }
  blockquote, q {
    quotes: none;
  }
  blockquote:before, blockquote:after,
  q:before, q:after {
    content: '';
    content: none;
  }
  table {
    border-collapse: collapse;
    border-spacing: 0;
  }
  /* RESET STYLES END */

  /* CUSTOM STYLES BELOW */
  body {
    background: #f9f9f9;
  }

  #app {
    font-family: 'PT Sans', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 60px;
  }

  .container {
    max-width: 960px;
    margin: auto;
  }

  /* TYPOGRAPHY */
  h1 {
    font-size: 3em;
    margin-bottom: 0.2em;
    font-weight: bold;
  }

  h2 {
    font-size: 1.5em;
    margin-bottom: 0.5em;
  }

  h3 {
    font-size: 1em;
    margin-bottom: 0.5em;
  }
  /* END TYPOGRAPHY */

  .button {
    background: #f9f9f9;
    display: inline-block;
    line-height: 1em;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 1em;

    /*border: 1px solid black;*/
    text-decoration: none;

    border: 2px solid #bbb;
    color: #555;

    transition: all .2s ease-out;

    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently */
  }

  .button:hover {
    background: white;
    transform: translate(0, -2px);
    cursor: pointer;
  }

  .primary.button  {
    border: 2px solid #21ba45;
    color: white;
    background: #21ba45;
  }

  .primary.button:hover {
    background: #21ac44;
  }

  .button.big {
    font-size: 1.5em;
    padding: 15px 30px;
  }

  .button.huge {
    font-size: 2em;
    padding: 20px 40px;
  }

  .button.group {
    display: flex;
    flex-flow: row wrap;
    padding: 0 !important;
    align-items: stretch;
  }

  .button.group > .button {
    border-radius: 0;
    border: 0;
    object-fit: cover;
  }

  .button.group > .button:first-of-type {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
  }

  .button.group > .button:last-of-type {
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
  }

  .button.left.part:hover  {
    background: #22ad45;
    flex-grow: 1;
    text-align: center;
  }

  .button.right.part {
    background: #21a943;
    border-left: 1px solid #22b945;
  }

  .system {
    margin: 20px auto;
    font-size: 0.8em;
    padding: 10px;
    background: #eee;
    border-radius: 10px;
    width: 200px;
    text-align: center;
  }
</style>
