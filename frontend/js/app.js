// Inicializar mapa centrado en Los Mochis
const mapa = L.map("mapa", {
    zoomControl: false // Quitamos el control por defecto para moverlo si es necesario, o dejarlo así para limpieza
}).setView([25.7928058, -108.990188], 14);

// Marcador origen
const iconoOrigen = L.divIcon({
    className: "marcador-origen",
    html: `
        <div class="marcador-origen-icon">
            <i class="fa-solid fa-building"></i>
        </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
});

const marcadorOrigen = L.marker(
    [25.774814, -108.99837],
    {
        icon: iconoOrigen,
        zIndexOffset: 1000
    }
)
    .addTo(mapa)
    .bindPopup(`
        <div style="text-align: center;">
            <strong>Punto de origen</strong><br>
            <span style="color: #666; font-size: 12px;">
                Oficinas Productos Meza
            </span>
        </div>
    `);

// Zona 1
const zona1 = L.polygon([
    [25.772966, -109.000443],
    [25.784847, -109.004332],
    [25.804657, -109.038347],
    [25.817018, -109.029797],
    [25.843785, -108.981336],
    [25.823056, -108.965471]
], {
    color: "#2563eb",
    weight: 3,
    fillColor: "#2563eb",
    fillOpacity: 0.15
}).addTo(mapa);

zona1.bindTooltip("ZONA 1", {
    permanent: true,
    direction: "center",
    className: "etiqueta-zona"
});


// Zona 2
const zona2 = L.polygon([
    [25.772881, -109.000435],
    [25.755070, -108.969774],
    [25.801059, -108.943780],
    [25.823194, -108.965383]
], {
    color: "#16a34a",
    weight: 3,
    fillColor: "#16a34a",
    fillOpacity: 0.15
}).addTo(mapa);

zona2.bindTooltip("ZONA 2", {
    permanent: true,
    direction: "center",
    className: "etiqueta-zona"
});


// Zona 3
const zona3 = L.polygon([
    [25.772758, -109.000499],
    [25.756481, -108.972464],
    [25.725929, -108.993855],
    [25.741840, -109.021596]
], {
    color: "#eab308",
    weight: 3,
    fillColor: "#eab308",
    fillOpacity: 0.15
}).addTo(mapa);

zona3.bindTooltip("ZONA 3", {
    permanent: true,
    direction: "center",
    className: "etiqueta-zona"
});


// Zona 4
const zona4 = L.polygon([
    [25.772888, -109.000496],
    [25.785685, -109.005280],
    [25.804689, -109.038371],
    [25.788768, -109.048584],
    [25.747936, -109.041201],
    [25.740165, -109.023391]
], {
    color: "#dc2626",
    weight: 3,
    fillColor: "#dc2626",
    fillOpacity: 0.15
}).addTo(mapa);

zona4.bindTooltip("ZONA 4", {
    permanent: true,
    direction: "center",
    className: "etiqueta-zona"
});

// Agregar control de zoom en una posición diferente (opcional)
L.control.zoom({ position: 'topleft' }).addTo(mapa);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19
}).addTo(mapa);

let rutaActual = null;
let clientesDatos = []; // Para guardar el estado de los clientes
let marcadoresOrden = []; // Para guardar el orden de los marcadores

async function cargarClientes() {
    try {
        const respuesta = await fetch("http://127.0.0.1:8000/clientes/");

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los clientes");
        }

        clientesDatos = await respuesta.json();

    } catch (error) {
        console.error("Error al conectar con el backend:", error);

        alert(
            "No se pudo conectar con el servidor. " +
            "Verifica que FastAPI esté ejecutándose."
        );

        return;
    }

    const contenedorClientesRuta = document.getElementById("clientes-ruta");


    clientesDatos.forEach(cliente => {

        // Crear Marcadores
        const marcador = L.marker([cliente.latitud, cliente.longitud])
            .addTo(mapa)
            .bindPopup(`
                <div style="text-align: center;">
                    <strong>${cliente.nombre}</strong><br>
                    <span style="color: #666; font-size: 12px;">${cliente.telefono}</span><br>
                    <span style="font-size: 12px;">${cliente.direccion}</span>
                </div>
            `);
        cliente.marcador = marcador;

        crearElementoLista(
            cliente,
            contenedorClientesRuta
        );

    });

    ajustarMapa();
    actualizarContadorZona();
}

function crearElementoLista(cliente, contenedor) {

    const elemento = document.createElement("div");
    elemento.className = "cliente-ruta-item";

    elemento.innerHTML = `
        <input
            type="checkbox"
            value="${cliente.id}"
        >

        <span class="cliente-ruta-nombre">
            ${cliente.nombre}
            <small class="cliente-ruta-zona">
                ${cliente.zona ? `Zona ${cliente.zona}` : "Sin zona"}
            </small>
        </span>

        <button
            class="btn-eliminar"
            type="button"
            title="Eliminar cliente"
        >
            <i class="fa-regular fa-trash-can"></i>
        </button>
    `;

    const botonEliminar = elemento.querySelector(".btn-eliminar");

    botonEliminar.addEventListener("click", async (evento) => {
        evento.stopPropagation();

        const confirmar = confirm(
            `¿Seguro que quieres eliminar a ${cliente.nombre}?`
        );

        if (!confirmar) return;

        try {
            const respuesta = await fetch(
                `http://127.0.0.1:8000/clientes/${cliente.id}`,
                {
                    method: "DELETE"
                }
            );

            if (!respuesta.ok) {
                const resultado = await respuesta.json();

                alert(
                    resultado.detail ||
                    "No se pudo eliminar el cliente"
                );

                return;
            }

        } catch (error) {
            console.error(
                "Error al conectar con el backend:",
                error
            );

            alert(
                "No se pudo conectar con el servidor. " +
                "Verifica que FastAPI esté ejecutándose."
            );

            return;
        }

        if (cliente.marcador) {
            mapa.removeLayer(cliente.marcador);
        }

        elemento.remove();

        clientesDatos = clientesDatos.filter(
            c => c.id !== cliente.id
        );

        limpiarRutaUI();
    });

    contenedor.appendChild(elemento);
}

function ajustarMapa() {
    if (clientesDatos.length > 0) {
        const limites = L.latLngBounds(clientesDatos.map(c => [c.latitud, c.longitud]));
        mapa.fitBounds(limites, { padding: [50, 50] });
    }
}

function limpiarRutaUI() {
    if (rutaActual) {
        mapa.removeLayer(rutaActual);
        rutaActual = null;
    }
    document.getElementById("distancia").innerHTML = `<i class="fa-solid fa-route"></i> Distancia: -- km`;
    document.getElementById("duracion").innerHTML = `<i class="fa-regular fa-clock"></i> Tiempo: -- min`;

    marcadoresOrden.forEach(marcador => {
        mapa.removeLayer(marcador);
    });

    marcadoresOrden = [];
}

// ----------------------- EVENTOS DE INTERFAZ --------------------------------

document.getElementById("limpiar-ruta").addEventListener("click", limpiarRutaUI);

// ---------------------------------- RUTAS OPTIMIZADAS -------------------------------------------
async function calcularRutaOptimizada(clientesIds) {
    const respuesta = await fetch(
        "http://127.0.0.1:8000/rutas/optimizar",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                clientes: clientesIds
            })
        }
    );

    if (!respuesta.ok) {
        const resultado = await respuesta.json();

        throw new Error(
            resultado.detail || "No se pudo optimizar la ruta"
        );
    }

    return await respuesta.json();
}
// -------------------------------- BOTONES DE BUSCAR RUTA OPTIMIZADA ---------------------------------------------


document.getElementById("calcular-ruta").addEventListener("click", async () => {
    const clientesSeleccionados = obtenerClientesSeleccionados();

    if (clientesSeleccionados.length === 0) {
        alert("Selecciona al menos un cliente a visitar");
        return;
    }

    try {
        const ruta = await calcularRutaOptimizada(
            clientesSeleccionados
        );

        dibujarRuta(
            ruta.geometria.coordinates,
            ruta.distancia_metros,
            ruta.duracion_segundos
        );

        console.log("Orden optimizado:", ruta.orden);

        marcadoresOrden.forEach(marcador => {
            mapa.removeLayer(marcador);
        });

        marcadoresOrden = [];

        ruta.orden.forEach((cliente, indice) => {
            crearMarcadorOrden(
                indice + 1,
                cliente.latitud,
                cliente.longitud
            );
        });

    } catch (error) {
        console.error("Error al calcular la ruta:", error);

        alert(
            error.message ||
            "No se pudo calcular la ruta"
        );
    }
});

// ---------------------------------------------------------------------------------------

function dibujarRuta(coordsGeoJSON, distanciaMetros, duracionSegundos) {
    const distanciaKm = (distanciaMetros / 1000).toFixed(2);
    const minutos = Math.round(duracionSegundos / 60);

    document.getElementById("distancia").innerHTML = `<i class="fa-solid fa-route"></i> Distancia: ${distanciaKm} km`;
    document.getElementById("duracion").innerHTML = `<i class="fa-regular fa-clock"></i> Tiempo: ${minutos} min`;

    // Leaflet usa [Lat, Lng], GeoJSON devuelve [Lng, Lat]
    const coordenadasLatLng = coordsGeoJSON.map(coord => [coord[1], coord[0]]);

    if (rutaActual) mapa.removeLayer(rutaActual);

    rutaActual = L.polyline(coordenadasLatLng, { color: '#3b82f6', weight: 4 }).addTo(mapa);
    mapa.fitBounds(rutaActual.getBounds(), { padding: [50, 50] });
}

document.getElementById("crear-cliente").addEventListener("click", async () => {
    const nombre = document.getElementById("nombre-cliente").value;
    const telefono = document.getElementById("telefono-cliente").value;
    const tipoVialidad = document.getElementById("tipo-vialidad").value;
    const nombreVialidad = document.getElementById("nombre-vialidad").value;
    const numeroVialidad = document.getElementById("numero-vialidad").value;
    const colonia = document.getElementById("colonia-cliente").value;

    const direccion = `${tipoVialidad} ${nombreVialidad} ${numeroVialidad}, ${colonia}, Los Mochis, Sinaloa, México`;

    if (!nombre || !telefono || !nombreVialidad || !numeroVialidad || !colonia) {
        alert("Completa todos los campos");
        return;
    }

    let nuevoCliente = {
        nombre: nombre,
        telefono: telefono,
        direccion: direccion
    };

    try {
        const respuesta = await fetch(
            "http://127.0.0.1:8000/clientes/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(nuevoCliente)
            }
        );

        if (!respuesta.ok) {
            const resultado = await respuesta.json();

            alert(
                resultado.detail || "No se pudo crear el cliente"
            );

            return;
        }

        nuevoCliente = await respuesta.json();

        

    } catch (error) {
        console.error("Error al conectar con el backend:", error);

        alert(
            "No se pudo conectar con el servidor. " +
            "Verifica que FastAPI esté ejecutándose."
        );

        return;
    }

    clientesDatos.push(nuevoCliente);

        // Obtener la zona actualmente seleccionada
        const zonaSeleccionada =
            document.getElementById("filtro-zona").value;

        const perteneceAZona =
            zonaSeleccionada === "todas" ||
            String(nuevoCliente.zona) === zonaSeleccionada;

        // Agregar marcador
        nuevoCliente.marcador = L.marker([
            nuevoCliente.latitud,
            nuevoCliente.longitud
        ])
            .bindPopup(`
                <div style="text-align: center;">
                    <strong>${nuevoCliente.nombre}</strong><br>
                    <span style="color: #666; font-size: 12px;">
                        ${nuevoCliente.telefono}
                    </span><br>
                    <span style="font-size: 12px;">
                        ${nuevoCliente.direccion}
                    </span>
                </div>
            `);

        if (perteneceAZona) {
            nuevoCliente.marcador.addTo(mapa);
        }


        // Agregar a "Clientes a visitar"
        const contenedorClientesRuta =
            document.getElementById("clientes-ruta");

        crearElementoLista(
            nuevoCliente,
            contenedorClientesRuta
        );


        // Mostrar u ocultar el elemento según la zona
        const ultimoElemento =
            contenedorClientesRuta.lastElementChild;

        if (perteneceAZona) {
            ultimoElemento.style.display = "flex";
        } else {
            ultimoElemento.style.display = "none";
        }


    // Limpiar inputs
    document.getElementById("nombre-cliente").value = "";
    document.getElementById("telefono-cliente").value = "";
    document.getElementById("nombre-vialidad").value = "";
    document.getElementById("numero-vialidad").value = "";
    document.getElementById("colonia-cliente").value = "";

    alert("Cliente creado correctamente");

});

// Obtiene el ID de los clientes seleccionados en la checklist
function obtenerClientesSeleccionados() {
    const checkboxes = document.querySelectorAll(
        '#clientes-ruta input[type="checkbox"]:checked'
    );

    return Array.from(checkboxes).map(checkbox => Number(checkbox.value));
}

// Inicializar
cargarClientes();

function actualizarContadorZona() {
    const zonaSeleccionada =
        document.getElementById("filtro-zona").value;

    const clientesVisibles = clientesDatos.filter(cliente => {
        return (
            zonaSeleccionada === "todas" ||
            String(cliente.zona) === zonaSeleccionada
        );
    });

    document.getElementById("contador-zona").textContent =
        `Clientes disponibles: ${clientesVisibles.length}`;
}


document.getElementById("filtro-zona").addEventListener("change", function () {

    const zonaSeleccionada = this.value;

    ajustarZoomZona(zonaSeleccionada);

    [zona1, zona2, zona3, zona4].forEach((zona, indice) => {
        const numeroZona = String(indice + 1);

        if (
            zonaSeleccionada === "todas" ||
            zonaSeleccionada === numeroZona
        ) {
            zona.addTo(mapa);
        } else {
            zona.removeFrom(mapa);
        }
    });

//----------------------------------------------------

    function ajustarZoomZona(zonaSeleccionada) {

    if (zonaSeleccionada === "todas") {
        const limitesGenerales = L.latLngBounds([]);

        [zona1, zona2, zona3, zona4].forEach(zona => {
            limitesGenerales.extend(zona.getBounds());
        });

        mapa.fitBounds(limitesGenerales, {
            padding: [50, 50]
        });

        return;
    }

    const zonas = {
        "1": zona1,
        "2": zona2,
        "3": zona3,
        "4": zona4
    };

    const zona = zonas[zonaSeleccionada];

    if (zona) {
        mapa.fitBounds(zona.getBounds(), {
            padding: [50, 50]
        });
    }
}


// --------------------------------------------------

    const elementos =
        document.querySelectorAll(".cliente-ruta-item");

    elementos.forEach(elemento => {
        const checkbox =
            elemento.querySelector("input[type='checkbox']");

        const clienteId = Number(checkbox.value);

        const cliente = clientesDatos.find(
            c => c.id === clienteId
        );

        const perteneceAZona =
            zonaSeleccionada === "todas" ||
            String(cliente.zona) === zonaSeleccionada;

        if (perteneceAZona) {
            elemento.style.display = "flex";
            cliente.marcador.addTo(mapa);
        } else {
            checkbox.checked = false;
            elemento.style.display = "none";
            cliente.marcador.removeFrom(mapa);
        }
    });

    actualizarContadorZona();
});

// Hace la enumeracion al orden de la ruta (1, 2, 3, etc)
function crearMarcadorOrden(numero, latitud, longitud) {
    const icono = L.divIcon({
        className: "marcador-orden",
        html: `
            <div class="marcador-orden-numero">
                ${numero}
            </div>
        `,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
    });

    const marcador = L.marker(
        [latitud, longitud],
        {
            icon: icono,
            zIndexOffset: 1000
        }
    ).addTo(mapa);

    marcadoresOrden.push(marcador);

    return marcador;
}
