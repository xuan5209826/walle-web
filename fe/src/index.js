// import 'core-js/fn/object/assign';
import React from 'react';
import { render } from 'react-dom';
import { Router, browserHistory } from 'react-router';
import NProgress from 'nprogress';
require('nprogress/nprogress.css');
require('styles/index.css');

const rootRoute = {
    path: '/',
    // 该组件需要使用 module.exports
    indexRoute: {
        getComponent(nextState, cb) {
            require.ensure([], (require) => {
                cb(null, require('components/page/HomePage').default);
            }, 'homePage');
        },
    },
    getComponent(nextState, cb) {
        require.ensure([], (require) => {
            cb(null, require('components/App').default);
        }, 'app');
    },
    childRoutes: [
        require('./routes/config'),
        require('./routes/project'),
    ],

    onEnter() {
        NProgress.start();
    },
};

// Render the main component into the dom
render(
  (
    <Router
      history={browserHistory}
      routes={rootRoute}
    />
  ), document.getElementById('root')
);
