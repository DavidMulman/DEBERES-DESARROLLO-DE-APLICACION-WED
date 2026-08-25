document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formTecnologia");

    if (!formulario) return;

    const lista = document.getElementById("lista");
    const mensaje = document.getElementById("mensaje");
    const total = document.getElementById("total");
    let contador = 0;

    formulario.addEventListener("submit", function (event) {
        event.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const descripcion = document.getElementById("descripcion").value.trim();
        const categoria = document.getElementById("categoria").value.trim();

        if (nombre.length < 3 || descripcion.length < 5 || categoria.length < 3) {
            mensaje.innerHTML = `
                <div class="alert alert-danger">
                    Verifique los datos. El nombre y la categoría deben tener al menos 3 caracteres
                    y la descripción al menos 5 caracteres.
                </div>`;
            return;
        }

        const card = document.createElement("div");
        card.className = "card shadow p-3 mb-3";
        card.innerHTML = `
            <h5>${nombre}</h5>
            <p>${descripcion}</p>
            <span class="badge bg-primary mb-2">${categoria}</span>
        `;

        const boton = document.createElement("button");
        boton.className = "btn btn-danger btn-sm";
        boton.textContent = "Eliminar";

        boton.addEventListener("click", function () {
            card.remove();
            contador--;
            total.textContent = contador;
        });

        card.appendChild(boton);
        lista.appendChild(card);

        contador++;
        total.textContent = contador;

        mensaje.innerHTML = `
            <div class="alert alert-success">
                Registro agregado correctamente.
            </div>`;

        formulario.reset();
    });
});

function validarContacto(event) {
    event.preventDefault();
    alert("Información enviada correctamente. Esta versión es demostrativa.");
    return false;
}
