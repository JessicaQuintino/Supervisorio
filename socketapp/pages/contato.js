import React from "react";
import esteira from './esteira.png';

const Contato = () => (
    <div className="title">
        <h4>Contato</h4>
        <p>Página de contato.</p>
        <div className="esteira">
          <img src={esteira}/>
        </div>
    </div>
);

export default Contato;