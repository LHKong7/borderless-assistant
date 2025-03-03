import React from 'react'
import ReactDOM from 'react-dom'

import RecordButton from './components/RecordButton';
// import Header from './components/Header/Header'
// import Editor from './components/Editor/Editor'
// import Ticker from './components/Ticker/Ticker'

import './index.css'

const App = function() {
  return (
    <div className='container'>
      <div id="stars"></div>
      <div id="stars2"></div>
      <div id="stars3"></div>
      <div id="content">
        <div className='response'></div>
        <RecordButton />
      </div>
    </div>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)