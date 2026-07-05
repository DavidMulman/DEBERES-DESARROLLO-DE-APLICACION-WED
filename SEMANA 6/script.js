const formulario = document.getElementById("formTecnologia");
const lista = document.getElementById("lista");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value.trim();

    if(nombre==="" || descripcion==="" || categoria===""){

        mensaje.innerHTML=`
        <div class="alert alert-danger">
            Todos los campos son obligatorios.
        </div>
        `;

        return;
    }

    mensaje.innerHTML=`
    <div class="alert alert-success">
        Registro agregado correctamente.
    </div>
    `;

    const card=document.createElement("div");

    card.className="card shadow p-3 mb-3";

    card.innerHTML=`
        <h5>${nombre}</h5>
        <p>${descripcion}</p>
        <span class="badge bg-primary mb-2">${categoria}</span>
    `;

    const boton=document.createElement("button");

    boton.textContent="Eliminar";

    boton.className="btn btn-danger";

    boton.addEventListener("click",function(){

        card.remove();

        contador--;

        total.textContent=contador;

    });

    card.appendChild(boton);

    lista.appendChild(card);

    contador++;

    total.textContent=contador;

    formulario.reset();

});