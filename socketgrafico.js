import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import io from 'socket.io-client'; 
import React from 'react';
import ReactDOM from 'react-dom';
import {useEffect,useState} from 'react';
import {Line,LineChart,XAxis,YAxis } from "recharts";
import socket from "socket.io-client/lib/socket";

class Grafico extends React.Component{
    
 state = {
        freq_des: '',
        freq_mot:"",
        tensao:"",
        rotacao:'',
        pot_entrada:"",
        corrente:"",
        temp_estator:"",
        vel_esteira:"",
        carga:"",
        peso_obj:"",
        vetorDados:[],
        socketStatus:"On"
    }  
    componentWillUnmount() {
        this.socket.close()
        console.log("component unmounted")
    }
    componentDidMount() {
        var sensorEndpoint = "http://localhost:5000"
        var vetorDados=[];
            this.socket = io.connect(sensorEndpoint, {
            reconnection: true,
        });
            this.socket.on("responseMessage", message => {
                this.setState({'freq_des': message.freq_des,'freq_mot':message.freq_mot/10,'tensao':message.tensao,'rotacao':message.rotacao,'pot_entrada':message.pot_entrada,'corrente':message.corrente/10,'temp_estator':message.temp_estator/10,'vel_esteira':message.vel_esteira/10,'carga':message.carga,'peso_obj':message.peso_obj,'dado1':vetorDados.push(message.rotacao)})
                console.log(vetorDados.length)
           })
            
    }

    render(){
        return(
            <React.Fragment>
                <div className="title">
                    <div style={{textAlign:"center"}}>
                        <p><h2>Rotação</h2>{this.state.vetorDados} RPM</p>
                        <LineChart width={800} height={600} data={this.state.vetorDados}>
                            <XAxis/>
                            <YAxis/>
                            <Line dataKey="dado1"/>
                        </LineChart>
                    </div>
                </div>
            </React.Fragment>
        );
    }

    
}

export default Grafico;