import React from 'react';
import ReactDOM from 'react-dom';
import { Nav, NavList, App } from './nav.jsx';
// import '~antd/dist/antd.css';

// ReactDOM.render(
//   (
//     <div>
//       <Nav item="Salary table" />
//       <Nav item="Google trends" />
//       <Nav item="Job listings" />
//     </div>
//   ),
//   document.getElementById('navbar')
// );


ReactDOM.render(<App />, document.getElementById('navbar2'));



window.React = React;
window.ReactDOM = ReactDOM;
window.NavList = NavList;