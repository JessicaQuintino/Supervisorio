import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route,Switch} from 'react-router-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import pageHome from './pages/Home';
import grafico from './pages/Graficopage';
import Contato from './pages/contato';

ReactDOM.render(
    (
      <Router>
        <App>
          <Switch>
              <Route exact path="/" component={pageHome}/>
              <Route path ="/grafico" component={grafico}/>
            <Route path="/contato" component={Contato}/>
          </Switch>
        </App>
      </Router>
    ),
    document.getElementById('root')
  );
  serviceWorker.unregister();
