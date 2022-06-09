import React from "react";
import io from 'socket.io-client'; 
import { Component } from "react/cjs/react.production.min";
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import esteira from './esteira.png';

class Dashboard extends React.Component {
    state = {
        freq_des: "",
        freq_mot:"",
        tensao:"",
        rotacao:"",
        pot_entrada:"",
        corrente:"",
        temp_estator:"",
        vel_esteira:"",
        carga:"",
        peso_obj:"",
        socketStatus:"On"
    }
    componentWillUnmount() {
        this.socket.close()
        console.log("component unmounted")
    }
    componentDidMount() {
        var sensorEndpoint = "http://localhost:5000"
            this.socket = io.connect(sensorEndpoint, {
            reconnection: true,
            // transports: ['websocket']
        });
        console.log("component mounted")
            this.socket.on("responseMessage", message => {
                this.setState({'freq_des': message.freq_des,'freq_mot':message.freq_mot/10,'tensao':message.tensao,'rotacao':message.rotacao,'pot_entrada':message.pot_entrada,'corrente':message.corrente/10,'temp_estator':message.temp_estator/10,'vel_esteira':message.vel_esteira/10,'carga':message.carga,'peso_obj':message.peso_obj})
                
                //console.log("responseMessage", message)
            })
            
    }
    handleEmit=()=>{
        if(this.state.socketStatus==="On"){
        this.socket.emit("message", {'data':'Stop Sending', 'status':'Off'})
        this.setState({'socketStatus':"Off"})
    }
    else{        
        this.socket.emit("message", {'data':'Start Sending', 'status':'On'})
        this.setState({'socketStatus':"On"})
        }
        console.log("Emit Clicked")
    }

    render() {
        return (
            <React.Fragment>
                <div>
                    <main className="main_lista">
                    <p><h3>Informações sistema esteira industrial</h3></p>
                        <div className="conteudo_listagem">
                            <div className="listas">
                                <ul className="listagem">
                                <li className="itens"><h2>Frequência escrita</h2>{this.state.freq_des} Hz</li>
                                <li className="itens"><h2>Frequência motor</h2>{this.state.freq_mot} Hz</li>
                                <li className="itens"><h2>Tensão</h2>{this.state.tensao} V</li>
                                </ul>
                                <ul className="listagem">
                                <li className="itens"><h2>Rotação</h2>{this.state.rotacao} RPM</li>
                                <li className="itens"><h2>Potência entrada</h2>{this.state.pot_entrada} kW</li>
                                <li className="itens"><h2>Corrente</h2>{this.state.corrente} A</li>
                                </ul>
                                <ul className="listagem">
                                <li className="itens"><h2>Temperatura estator</h2>{this.state.temp_estator} ºC</li>
                                <li className="itens"><h2>Velocidade Esteira</h2>{this.state.vel_esteira} m/s</li>
                                <li className="itens"><h2>Carga</h2>{this.state.carga}</li>
                                <li className="itens"><h2>Peso</h2>{this.state.peso_obj} Kg</li>
                                </ul>
                                </div>
                                <img className="imagem" src={esteira}/>
                            </div>
                        </main>
                        <ul>
                    <div onClick={this.handleEmit}> Start/Stop</div>
                    <input type="text" onInput={this.state.freq_des}></input>
                    <button onClick={this.handleClick}>Clique Aqui!</button>
                    </ul>
                </div>
            </React.Fragment>
        );
    }
}
export default Dashboard;