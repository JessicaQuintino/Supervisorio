import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Dashboard from './socketDashboard';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import {Menubar} from 'primereact/menubar';
import Header from './components/header';
import Footer from './components/footer';
import {withRouter} from 'react-router-dom';



class App extends Component{
  render(){
    const menuitems = [
      {
          label:'Home',
          icon:'pi pi-fw pi-home',
          command:() => this.props.history.push('/')  
      },
      {
          label:'Gráfico',
          icon:'pi pi-fw pi-chart-bar',
          command:() => this.props.history.push('/Grafico')
      },
      {
          label:'Contato',
          icon:'pi pi-fw pi-comment',
          command:() => this.props.history.push('/contato')
      }
  ]

    return <div>
      <Menubar model={menuitems} className="content"/>
      <div id="main">
        <main>
          <div className="content" id="content">
              {this.props.children}
          </div>
         </main>
         <div>
      <Header/>
      <Footer/>
      </div>
      </div>
    </div>
    
  }
}

export default withRouter(App);
