import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Open City 3D",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: 0 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0,
               maximum-scale=1.0, user-scalable=no">

<title>Open City 3D</title>

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050816;
    font-family: Arial, Helvetica, sans-serif;
    user-select: none;
}

#game {
    position: fixed;
    inset: 0;
}

canvas {
    display: block;
}

#loading {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background:
        radial-gradient(circle at 50% 30%, #263d70, #050816 70%);
    color: white;
    text-align: center;
}

#loading h1 {
    font-size: 42px;
    margin: 0 0 10px;
    text-shadow: 0 0 25px #60a5fa;
}

#loading p {
    color: #cbd5e1;
}

.loader {
    width: 260px;
    height: 8px;
    background: #1e293b;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 15px;
}

.loader div {
    width: 0%;
    height: 100%;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #6366f1,
        #a855f7
    );
    transition: width .25s;
}

#error {
    display: none;
    max-width: 500px;
    color: #fecaca;
    background: rgba(127,29,29,.8);
    border: 1px solid #ef4444;
    border-radius: 12px;
    padding: 15px;
    margin-top: 20px;
}

#startScreen {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 90;
    align-items: center;
    justify-content: center;
    background: rgba(2,6,23,.25);
}

.panel {
    width: min(440px, 90%);
    padding: 30px;
    text-align: center;
    color: white;
    background: rgba(15,23,42,.86);
    border: 1px solid rgba(148,163,184,.3);
    border-radius: 20px;
    box-shadow:
        0 25px 80px rgba(0,0,0,.6),
        inset 0 1px rgba(255,255,255,.1);
    backdrop-filter: blur(15px);
}

.panel h1 {
    margin-top: 0;
    font-size: 36px;
}

.panel p {
    color: #cbd5e1;
    line-height: 1.6;
}

.mainButton {
    border: 0;
    border-radius: 12px;
    padding: 14px 28px;
    color: white;
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(37,99,235,.35);
}

.mainButton:hover {
    transform: translateY(-1px);
}

#hud {
    position: fixed;
    left: 15px;
    top: 15px;
    z-index: 20;
    min-width: 190px;
    color: white;
    background: rgba(2,6,23,.68);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 14px;
    padding: 13px 15px;
    box-shadow: 0 10px 35px rgba(0,0,0,.25);
    backdrop-filter: blur(10px);
}

.row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    margin: 4px 0;
}

.value {
    font-weight: bold;
}

#healthBar {
    width: 100%;
    height: 7px;
    background: #334155;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 6px;
}

#healthFill {
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        #ef4444,
        #22c55e
    );
}

#wanted {
    color: #facc15;
}

#mission {
    color: #fbbf24;
}

#help {
    position: fixed;
    right: 15px;
    top: 15px;
    z-index: 20;
    color: #e2e8f0;
    background: rgba(2,6,23,.62);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 12px;
    padding: 10px 13px;
    font-size: 13px;
    line-height: 1.6;
    backdrop-filter: blur(8px);
}

#message {
    position: fixed;
    left: 50%;
    bottom: 28px;
    transform: translateX(-50%);
    z-index: 30;
    max-width: 90%;
    color: white;
    background: rgba(2,6,23,.78);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 12px;
    padding: 10px 18px;
    text-align: center;
    opacity: 0;
    transition: opacity .2s;
}

#crosshair {
    position: fixed;
    left: 50%;
    top: 50%;
    z-index: 15;
    color: rgba(255,255,255,.8);
    font-size: 20px;
    transform: translate(-50%,-50%);
    pointer-events: none;
}

#minimap {
    position: fixed;
    right: 15px;
    bottom: 15px;
    width: 170px;
    height: 170px;
    z-index: 20;
    border-radius: 14px;
    overflow: hidden;
    background: rgba(2,6,23,.75);
    border: 2px solid rgba(255,255,255,.15);
}

#mapCanvas {
    width: 100%;
    height: 100%;
}

#mobileControls {
    display: none;
    position: fixed;
    left: 15px;
    bottom: 20px;
    z-index: 50;
}

.touchRow {
    display: flex;
    justify-content: center;
}

.touchButton {
    width: 55px;
    height: 55px;
    margin: 3px;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px;
    background: rgba(15,23,42,.75);
    color: white;
    font-size: 21px;
}

#actionButton {
    position: fixed;
    right: 200px;
    bottom: 20px;
    z-index: 50;
    display: none;
    width: 70px;
    height: 55px;
    border: 0;
    border-radius: 13px;
    color: white;
    background: #16a34a;
    font-weight: bold;
}

#gameOver {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 80;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,.7);
    color: white;
    text-align: center;
}

#gameOver h1 {
    font-size: 50px;
    color: #ef4444;
}

@media(max-width:700px) {

    #help {
        display: none;
    }

    #hud {
        left: 8px;
        top: 8px;
        min-width: 165px;
        font-size: 13px;
    }

    #minimap {
        width: 120px;
        height: 120px;
        right: 8px;
        bottom: 8px;
    }

    #mobileControls {
        display: block;
    }

    #actionButton {
        display: block;
        right: 140px;
    }
}
</style>
</head>

<body>

<div id="game"></div>

<div id="loading">
    <h1>🌆 OPEN CITY</h1>
    <p id="loadingText">Đang tải thành phố 3D...</p>
    <div class="loader">
        <div id="loadingBar"></div>
    </div>

    <div id="error"></div>
</div>

<div id="startScreen">
    <div class="panel">
        <h1>🌆 Open City 3D</h1>

        <p>
            Khám phá thành phố, lái xe,
            hoàn thành nhiệm vụ và tránh cảnh sát.
        </p>

        <p>
            <b>WASD</b> di chuyển<br>
            <b>E</b> vào / ra xe<br>
            <b>Shift</b> chạy nhanh<br>
            <b>Chuột</b> xoay camera
        </p>

        <button class="mainButton" id="startButton">
            ▶ BẮT ĐẦU
        </button>
    </div>
</div>

<div id="hud">

    <div class="row">
        <span>❤️ Máu</span>
        <span class="value" id="healthText">100</span>
    </div>

    <div id="healthBar">
        <div id="healthFill"></div>
    </div>

    <div class="row">
        <span>💰 Tiền</span>
        <span class="value">$<span id="money">100</span></span>
    </div>

    <div class="row">
        <span>⭐ Truy nã</span>
        <span class="value" id="wanted">0</span>
    </div>

    <div class="row">
        <span>🚗</span>
        <span class="value" id="vehicle">Đi bộ</span>
    </div>

    <div class="row">
        <span>📦</span>
        <span class="value" id="mission">---</span>
    </div>

</div>

<div id="help">
    <b>W A S D</b> — di chuyển<br>
    <b>Shift</b> — chạy nhanh<br>
    <b>E</b> — vào / ra xe<br>
    <b>Chuột trái + kéo</b> — xoay camera<br>
    <b>R</b> — chơi lại
</div>

<div id="crosshair">+</div>

<div id="message"></div>

<div id="minimap">
    <canvas id="mapCanvas" width="170" height="170"></canvas>
</div>

<div id="mobileControls">
    <div class="touchRow">
        <button class="touchButton" data-key="w">▲</button>
    </div>

    <div class="touchRow">
        <button class="touchButton" data-key="a">◀</button>
        <button class="touchButton" data-key="s">▼</button>
        <button class="touchButton" data-key="d">▶</button>
    </div>
</div>

<button id="actionButton">🚗 E</button>

<div id="gameOver">
    <div>
        <h1>GAME OVER</h1>
        <p>Bạn đã bị hạ.</p>
        <button class="mainButton" onclick="location.reload()">
            🔄 CHƠI LẠI
        </button>
    </div>
</div>


<script>

let THREE_READY = false;

/*
   Load Three.js safely.
*/
function loadThree() {

    const script =
        document.createElement("script");

    script.src =
        "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js";

    script.onload = () => {

        THREE_READY = true;

        setLoading(
            100,
            "Đã tải engine 3D!"
        );

        setTimeout(
            prepareGame,
            300
        );

    };

    script.onerror = () => {

        showError(
            "Không tải được Three.js. " +
            "Hãy kiểm tra kết nối Internet của " +
            "Streamlit Cloud rồi Deploy lại."
        );

    };

    document.head.appendChild(script);

}


function setLoading(percent,text) {

    document.getElementById(
        "loadingBar"
    ).style.width = percent + "%";

    document.getElementById(
        "loadingText"
    ).innerText = text;

}


function showError(text) {

    document.getElementById(
        "loadingText"
    ).innerText = "Không thể khởi động game";

    const error =
        document.getElementById("error");

    error.innerText = text;
    error.style.display = "block";

}


/* =========================================
   GAME
========================================= */

let scene;
let camera;
let renderer;

let player;
let playerMesh;

let cars = [];
let police = [];
let npcs = [];
let buildings = [];
let lamps = [];

let mission = null;

let running = false;
let gameOver = false;

let health = 100;
let money = 100;
let wanted = 0;

let keys = {};

let cameraYaw = 0.7;
let cameraDistance = 13;

let mouseDragging = false;

let lastTime = performance.now();

const WORLD_SIZE = 520;


/* =========================================
   PREPARE
========================================= */

function prepareGame() {

    if(!THREE_READY) return;

    try {

        createScene();

        setLoading(
            40,
            "Đang xây dựng thành phố..."
        );

        createCity();

        setLoading(
            75,
            "Đang tạo nhân vật..."
        );

        createPlayer();

        createMission();

        setupInput();

        drawMinimap();

        setLoading(
            100,
            "Sẵn sàng!"
        );

        setTimeout(() => {

            document.getElementById(
                "loading"
            ).style.display = "none";

            document.getElementById(
                "startScreen"
            ).style.display = "flex";

        },500);

    } catch(error) {

        showError(
            "Game gặp lỗi: " +
            error.message
        );

        console.error(error);

    }

}


/* =========================================
   SCENE
========================================= */

function createScene() {

    scene = new THREE.Scene();

    scene.background =
        new THREE.Color(0x8ec5f5);

    scene.fog =
        new THREE.Fog(
            0x8ec5f5,
            130,
            430
        );


    camera =
        new THREE.PerspectiveCamera(
            65,
            window.innerWidth /
            window.innerHeight,
            0.1,
            1000
        );


    renderer =
        new THREE.WebGLRenderer({
            antialias: true,
            powerPreference: "high-performance"
        });

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

    renderer.setPixelRatio(
        Math.min(
            window.devicePixelRatio || 1,
            1.5
        )
    );

    renderer.shadowMap.enabled = true;

    renderer.shadowMap.type =
        THREE.PCFSoftShadowMap;

    renderer.outputColorSpace =
        THREE.SRGBColorSpace;

    document
        .getElementById("game")
        .appendChild(renderer.domElement);


    /*
       Lighting
    */

    const hemi =
        new THREE.HemisphereLight(
            0xbddcff,
            0x304020,
            1.7
        );

    scene.add(hemi);


    const sun =
        new THREE.DirectionalLight(
            0xfff2d0,
            2.2
        );

    sun.position.set(
        100,
        180,
        80
    );

    sun.castShadow = true;

    sun.shadow.mapSize.width = 1024;
    sun.shadow.mapSize.height = 1024;

    sun.shadow.camera.left = -180;
    sun.shadow.camera.right = 180;
    sun.shadow.camera.top = 180;
    sun.shadow.camera.bottom = -180;

    scene.add(sun);


    /*
       Sun glow
    */

    const sunSphere =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                12,
                16,
                16
            ),
            new THREE.MeshBasicMaterial({
                color: 0xfff3b0
            })
        );

    sunSphere.position.set(
        -180,
        150,
        -250
    );

    scene.add(sunSphere);


    window.addEventListener(
        "resize",
        resize
    );

}


/* =========================================
   CITY
========================================= */

function createCity() {

    createGround();

    createRoads();

    createBuildings();

    createTrees();

    createStreetLights();

    createCars();

    createNPCs();

}


/* =========================================
   GROUND
========================================= */

function createGround() {

    const geometry =
        new THREE.PlaneGeometry(
            WORLD_SIZE,
            WORLD_SIZE
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x4f8c48,
            roughness: 1
        });

    const ground =
        new THREE.Mesh(
            geometry,
            material
        );

    ground.rotation.x =
        -Math.PI / 2;

    ground.receiveShadow = true;

    scene.add(ground);

}


/* =========================================
   ROADS
========================================= */

function createRoads() {

    for(
        let p = -240;
        p <= 240;
        p += 80
    ) {

        const vertical =
            new THREE.Mesh(
                new THREE.PlaneGeometry(
                    20,
                    WORLD_SIZE
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x30343b,
                    roughness: .95
                })
            );

        vertical.rotation.x =
            -Math.PI / 2;

        vertical.position.set(
            p,
            .02,
            0
        );

        scene.add(vertical);


        const horizontal =
            new THREE.Mesh(
                new THREE.PlaneGeometry(
                    WORLD_SIZE,
                    20
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x30343b,
                    roughness: .95
                })
            );

        horizontal.rotation.x =
            -Math.PI / 2;

        horizontal.position.set(
            0,
            .025,
            p
        );

        scene.add(horizontal);


        /*
           Lane markings
        */

        createLaneLine(
            p,
            0,
            true
        );

        createLaneLine(
            0,
            p,
            false
        );

    }

}


/* =========================================
   LANE LINE
========================================= */

function createLaneLine(
    x,
    z,
    vertical
) {

    const geometry =
        new THREE.BoxGeometry(
            vertical ? .18 : 20,
            .06,
            vertical ? 20 : .18
        );

    const material =
        new THREE.MeshBasicMaterial({
            color: 0xfacc15
        });

    for(
        let i = -240;
        i <= 240;
        i += 32
    ) {

        const line =
            new THREE.Mesh(
                geometry,
                material
            );

        if(vertical) {

            line.position.set(
                x,
                .09,
                i
            );

        } else {

            line.position.set(
                i,
                .09,
                z
            );

        }

        scene.add(line);

    }

}


/* =========================================
   BUILDINGS
========================================= */

function createBuildings() {

    const colors = [
        0x475569,
        0x64748b,
        0x52525b,
        0x57534e,
        0x334155,
        0x3f3f46
    ];


    for(
        let x = -220;
        x <= 220;
        x += 80
    ) {

        for(
            let z = -220;
            z <= 220;
            z += 80
        ) {

            /*
               Keep central roads clear.
            */

            if(
                Math.abs(x % 80) < 1 ||
                Math.abs(z % 80) < 1
            ) {
                continue;
            }


            const w =
                random(35,55);

            const d =
                random(35,55);

            const h =
                random(18,75);


            const geometry =
                new THREE.BoxGeometry(
                    w,
                    h,
                    d
                );

            const material =
                new THREE.MeshStandardMaterial({
                    color:
                        colors[
                            Math.floor(
                                Math.random() *
                                colors.length
                            )
                        ],
                    roughness: .85
                });


            const building =
                new THREE.Mesh(
                    geometry,
                    material
                );

            building.position.set(
                x + random(-8,8),
                h / 2,
                z + random(-8,8)
            );

            building.castShadow = true;
            building.receiveShadow = true;

            scene.add(building);

            buildings.push(building);


            /*
               Rooftop
            */

            if(Math.random() > .45) {

                const roof =
                    new THREE.Mesh(
                        new THREE.BoxGeometry(
                            w * .25,
                            2,
                            d * .25
                        ),
                        new THREE.MeshStandardMaterial({
                            color: 0x1e293b
                        })
                    );

                roof.position.set(
                    building.position.x,
                    h + 1,
                    building.position.z
                );

                scene.add(roof);

            }

        }

    }

}


/* =========================================
   TREES
========================================= */

function createTrees() {

    for(let i=0;i<90;i++) {

        const x =
            random(-245,245);

        const z =
            random(-245,245);


        const trunk =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    .8,
                    1.1,
                    6,
                    7
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x6b3f1d
                })
            );

        trunk.position.set(
            x,
            3,
            z
        );

        scene.add(trunk);


        const crown =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    random(3.5,5.5),
                    8,
                    8
                ),
                new THREE.MeshStandardMaterial({
                    color:
                        Math.random() > .5
                        ? 0x166534
                        : 0x15803d
                })
            );

        crown.position.set(
            x,
            8,
            z
        );

        crown.castShadow = true;

        scene.add(crown);

    }

}


/* =========================================
   STREET LIGHTS
========================================= */

function createStreetLights() {

    for(
        let p=-240;
        p<=240;
        p+=80
    ) {

        createLamp(
            p + 10,
            10
        );

        createLamp(
            -10,
            p + 10
        );

    }

}


function createLamp(x,z) {

    const pole =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                .12,
                .16,
                6,
                8
            ),
            new THREE.MeshStandardMaterial({
                color: 0x111827,
                metalness: .5
            })
        );

    pole.position.set(
        x,
        3,
        z
    );

    scene.add(pole);


    const lamp =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .45,
                8,
                8
            ),
            new THREE.MeshBasicMaterial({
                color: 0xfff0a0
            })
        );

    lamp.position.set(
        x,
        6.2,
        z
    );

    scene.add(lamp);

    lamps.push(lamp);

}


/* =========================================
   PLAYER
========================================= */

function createPlayer() {

    player = {
        x: 0,
        z: 0,
        speed: .18,
        inCar: false,
        car: null
    };


    playerMesh =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.CapsuleGeometry(
                .65,
                1.5,
                5,
                10
            ),
            new THREE.MeshStandardMaterial({
                color: 0x2563eb
            })
        );

    body.position.y = 1.4;

    body.castShadow = true;

    playerMesh.add(body);


    const head =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .58,
                12,
                12
            ),
            new THREE.MeshStandardMaterial({
                color: 0xf3c29f
            })
        );

    head.position.y = 3;

    head.castShadow = true;

    playerMesh.add(head);


    scene.add(playerMesh);

}


/* =========================================
   CARS
========================================= */

function createCars() {

    const colors = [
        0xef4444,
        0x3b82f6,
        0xeab308,
        0xa855f7,
        0xf97316,
        0x14b8a6,
        0xf43f5e,
        0xffffff
    ];


    for(let i=0;i<18;i++) {

        createCar(
            random(-230,230),
            random(-230,230),
            colors[
                Math.floor(
                    Math.random() *
                    colors.length
                )
            ]
        );

    }

}


function createCar(x,z,color) {

    const group =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                5,
                1.3,
                2.5
            ),
            new THREE.MeshStandardMaterial({
                color: color,
                metalness: .25,
                roughness: .55
            })
        );

    body.position.y = 1.05;

    body.castShadow = true;

    group.add(body);


    const cabin =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                2.6,
                1.05,
                2
            ),
            new THREE.MeshStandardMaterial({
                color: 0x172033,
                metalness: .1,
                roughness: .2
            })
        );

    cabin.position.set(
        -.25,
        1.95,
        0
    );

    group.add(cabin);


    /*
       Headlights
    */

    const lightMaterial =
        new THREE.MeshBasicMaterial({
            color: 0xffffee
        });


    const leftLight =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                .35,
                .3,
                .15
            ),
            lightMaterial
        );

    leftLight.position.set(
        2.52,
        1.05,
        -.75
    );

    group.add(leftLight);


    const rightLight =
        leftLight.clone();

    rightLight.position.z = .75;

    group.add(rightLight);


    /*
       Wheels
    */

    for(
        const zWheel of [-1.25,1.25]
    ) {

        for(
            const xWheel of [-1.65,1.65]
        ) {

            const wheel =
                new THREE.Mesh(
                    new THREE.CylinderGeometry(
                        .48,
                        .48,
                        .3,
                        12
                    ),
                    new THREE.MeshStandardMaterial({
                        color: 0x09090b
                    })
                );

            wheel.rotation.x =
                Math.PI / 2;

            wheel.position.set(
                xWheel,
                .55,
                zWheel
            );

            group.add(wheel);

        }

    }


    group.position.set(
        x,
        0,
        z
    );


    scene.add(group);


    const car = {
        mesh: group,
        x: x,
        z: z,
        occupied: false,
        police: false,
        speed: 0
    };


    cars.push(car);

    return car;

}


/* =========================================
   NPC
========================================= */

function createNPCs() {

    for(let i=0;i<25;i++) {

        const group =
            new THREE.Group();


        const body =
            new THREE.Mesh(
                new THREE.CapsuleGeometry(
                    .35,
                    .7,
                    4,
                    7
                ),
                new THREE.MeshStandardMaterial({
                    color:
                        randomColor()
                })
            );

        body.position.y = .9;

        group.add(body);


        const head =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    .3,
                    8,
                    8
                ),
                new THREE.MeshStandardMaterial({
                    color: 0xf2c19f
                })
            );

        head.position.y = 1.8;

        group.add(head);


        group.position.set(
            random(-230,230),
            0,
            random(-230,230)
        );


        scene.add(group);


        npcs.push({
            mesh: group,
            x: group.position.x,
            z: group.position.z,
            vx: random(-.025,.025),
            vz: random(-.025,.025)
        });

    }

}


/* =========================================
   MISSION
========================================= */

function createMission() {

    if(mission) {

        scene.remove(
            mission.mesh
        );

    }


    const mesh =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                3.5,
                3.5,
                .5,
                32
            ),
            new THREE.MeshStandardMaterial({
                color: 0xfacc15,
                emissive: 0x8a6500,
                emissiveIntensity: .5
            })
        );


    mesh.position.set(
        random(-180,180),
        .35,
        random(-180,180)
    );


    scene.add(mesh);


    mission = {
        mesh: mesh,
        reward:
            100 +
            Math.floor(
                Math.random()*300
            )
    };


    updateUI();

}


/* =========================================
   INPUT
========================================= */

function setupInput() {

    document.addEventListener(
        "keydown",
        function(e) {

            keys[
                e.key.toLowerCase()
            ] = true;


            if(
                e.key.toLowerCase() === "e"
            ) {
                enterExitCar();
            }


            if(
                e.key.toLowerCase() === "r"
            ) {
                location.reload();
            }

        }
    );


    document.addEventListener(
        "keyup",
        function(e) {

            keys[
                e.key.toLowerCase()
            ] = false;

        }
    );


    renderer.domElement.addEventListener(
        "mousedown",
        function() {
            mouseDragging = true;
        }
    );


    document.addEventListener(
        "mouseup",
        function() {
            mouseDragging = false;
        }
    );


    document.addEventListener(
        "mousemove",
        function(e) {

            if(!mouseDragging) return;

            cameraYaw -=
                e.movementX * .004;

        }
    );


    /*
       Touch buttons
    */

    document
        .querySelectorAll(
            ".touchButton"
        )
        .forEach(
            button => {

                const key =
                    button.dataset.key;


                button.addEventListener(
                    "pointerdown",
                    e => {

                        e.preventDefault();

                        keys[key] = true;

                    }
                );


                button.addEventListener(
                    "pointerup",
                    e => {

                        e.preventDefault();

                        keys[key] = false;

                    }
                );


                button.addEventListener(
                    "pointercancel",
                    () => {
                        keys[key] = false;
                    }
                );

            }
        );


    document.getElementById(
        "actionButton"
    ).addEventListener(
        "click",
        enterExitCar
    );


    document.getElementById(
        "startButton"
    ).addEventListener(
        "click",
        startGame
    );

}


/* =========================================
   PLAYER MOVEMENT
========================================= */

function updatePlayer(delta) {

    if(gameOver) return;


    let dx = 0;
    let dz = 0;


    if(keys["w"]) dz -= 1;
    if(keys["s"]) dz += 1;
    if(keys["a"]) dx -= 1;
    if(keys["d"]) dx += 1;


    if(dx === 0 && dz === 0) {
        return;
    }


    const length =
        Math.hypot(dx,dz);

    dx /= length;
    dz /= length;


    let speed =
        player.inCar
        ? 16
        : 7;


    if(keys["shift"]) {
        speed *= 1.55;
    }


    player.x +=
        dx * speed * delta;

    player.z +=
        dz * speed * delta;


    player.x =
        THREE.MathUtils.clamp(
            player.x,
            -245,
            245
        );

    player.z =
        THREE.MathUtils.clamp(
            player.z,
            -245,
            245
        );


    playerMesh.position.set(
        player.x,
        0,
        player.z
    );


    if(player.inCar &&
       player.car) {

        player.car.x = player.x;
        player.car.z = player.z;

        player.car.mesh.position.x =
            player.x;

        player.car.mesh.position.z =
            player.z;

        player.car.mesh.rotation.y =
            Math.atan2(dx,dz);

    }

}


/* =========================================
   NPC UPDATE
========================================= */

function updateNPCs(delta) {

    for(
        const npc of npcs
    ) {

        npc.x +=
            npc.vx * delta * 60;

        npc.z +=
            npc.vz * delta * 60;


        if(
            npc.x < -240 ||
            npc.x > 240
        ) {
            npc.vx *= -1;
        }


        if(
            npc.z < -240 ||
            npc.z > 240
        ) {
            npc.vz *= -1;
        }


        npc.mesh.position.x =
            npc.x;

        npc.mesh.position.z =
            npc.z;

    }

}


/* =========================================
   ENTER / EXIT CAR
========================================= */

function enterExitCar() {

    if(gameOver) return;


    if(player.inCar) {

        player.inCar = false;

        if(player.car) {
            player.car.occupied = false;
        }

        player.car = null;

        playerMesh.visible = true;

        document.getElementById(
            "vehicle"
        ).innerText = "Đi bộ";

        showMessage(
            "🚶 Bạn đã xuống xe."
        );

        return;

    }


    let nearest = null;
    let nearestDistance = 999;


    for(
        const car of cars
    ) {

        if(car.occupied) continue;

        const d =
            Math.hypot(
                car.x-player.x,
                car.z-player.z
            );


        if(d < nearestDistance) {

            nearestDistance = d;
            nearest = car;

        }

    }


    if(
        nearest &&
        nearestDistance < 8
    ) {

        player.inCar = true;
        player.car = nearest;

        nearest.occupied = true;

        playerMesh.visible = false;

        document.getElementById(
            "vehicle"
        ).innerText = "Đang lái";

        showMessage(
            "🚗 Đã vào xe!"
        );

    } else {

        showMessage(
            "🚗 Hãy đứng gần xe."
        );

    }

}


/* =========================================
   POLICE
========================================= */

function increaseWanted() {

    wanted =
        Math.min(
            5,
            wanted + 1
        );

    showMessage(
        "🚨 Truy nã tăng lên " +
        wanted + " sao!"
    );

}


function spawnPolice() {

    if(wanted < 1) return;

    if(
        police.length >=
        Math.ceil(wanted)
    ) {
        return;
    }


    const angle =
        Math.random() *
        Math.PI *
        2;

    const distance = 60;


    const car =
        createCar(
            player.x +
            Math.cos(angle) *
            distance,

            player.z +
            Math.sin(angle) *
            distance,

            0x1d4ed8
        );


    car.police = true;


    police.push(car);

}


function updatePolice(delta) {

    if(wanted <= 0) {

        return;

    }


    spawnPolice();


    for(
        const car of police
    ) {

        const dx =
            player.x-car.x;

        const dz =
            player.z-car.z;

        const distance =
            Math.hypot(dx,dz);


        if(distance > .1) {

            const speed =
                6 +
                wanted * 1.4;

            car.x +=
                dx/distance *
                speed *
                delta;

            car.z +=
                dz/distance *
                speed *
                delta;


            car.mesh.position.x =
                car.x;

            car.mesh.position.z =
                car.z;

            car.mesh.rotation.y =
                Math.atan2(
                    dx,
                    dz
                );

        }


        if(distance < 6) {

            health -=
                12 *
                delta;

            if(health <= 0) {

                health = 0;

                endGame();

            }

        }

    }

}


/* =========================================
   MISSION
========================================= */

function updateMission(delta) {

    if(!mission) return;


    mission.mesh.rotation.y +=
        delta * 2;


    const distance =
        Math.hypot(
            player.x -
            mission.mesh.position.x,

            player.z -
            mission.mesh.position.z
        );


    if(distance < 7) {

        money += mission.reward;


        showMessage(
            "📦 Nhiệm vụ hoàn thành! +" +
            "$" +
            mission.reward
        );


        scene.remove(
            mission.mesh
        );


        mission = null;


        setTimeout(
            createMission,
            1800
        );

    }

}


/* =========================================
   WANTED DECAY
========================================= */

function updateWanted(delta) {

    if(wanted > 0) {

        wanted -=
            delta * .015;


        if(wanted < 0) {
            wanted = 0;
        }

    }

}


/* =========================================
   CAMERA
========================================= */

function updateCamera() {

    const distance =
        player.inCar
        ? 16
        : 11;


    const height =
        player.inCar
        ? 8
        : 6.5;


    const target =
        new THREE.Vector3(
            player.x,
            player.inCar ? 1.5 : 2,
            player.z
        );


    const desired =
        new THREE.Vector3(
            player.x +
                Math.sin(cameraYaw) *
                distance,

            height,

            player.z +
                Math.cos(cameraYaw) *
                distance
        );


    camera.position.lerp(
        desired,
        .12
    );


    camera.lookAt(target);

}


/* =========================================
   UI
========================================= */

function updateUI() {

    document.getElementById(
        "healthText"
    ).innerText =
        Math.max(
            0,
            Math.floor(health)
        );


    document.getElementById(
        "healthFill"
    ).style.width =
        Math.max(
            0,
            health
        ) + "%";


    document.getElementById(
        "money"
    ).innerText =
        money;


    document.getElementById(
        "wanted"
    ).innerText =
        "⭐".repeat(
            Math.ceil(wanted)
        ) || "0";


    document.getElementById(
        "mission"
    ).innerText =
        mission
        ? "Đang làm"
        : "Đang tạo...";


    drawMinimap();

}


/* =========================================
   MINIMAP
========================================= */

function drawMinimap() {

    const canvas =
        document.getElementById(
            "mapCanvas"
        );

    if(!canvas) return;


    const ctx =
        canvas.getContext("2d");


    const w =
        canvas.width;

    const h =
        canvas.height;


    ctx.clearRect(
        0,
        0,
        w,
        h
    );


    ctx.fillStyle =
        "#172033";

    ctx.fillRect(
        0,
        0,
        w,
        h
    );


    /*
       Roads
    */

    ctx.fillStyle =
        "#374151";


    for(
        let p=-240;
        p<=240;
        p+=80
    ) {

        const x =
            (p+260) /
            520 *
            w;

        ctx.fillRect(
            x-3,
            0,
            6,
            h
        );


        const y =
            (p+260) /
            520 *
            h;

        ctx.fillRect(
            0,
            y-3,
            w,
            6
        );

    }


    /*
       Mission
    */

    if(mission) {

        const mx =
            (mission.mesh.position.x+260) /
            520 *
            w;

        const mz =
            (mission.mesh.position.z+260) /
            520 *
            h;


        ctx.fillStyle =
            "#facc15";

        ctx.beginPath();

        ctx.arc(
            mx,
            mz,
            5,
            0,
            Math.PI*2
        );

        ctx.fill();

    }


    /*
       Player
    */

    const px =
        (player.x+260) /
        520 *
        w;

    const pz =
        (player.z+260) /
        520 *
        h;


    ctx.fillStyle =
        "#22c55e";

    ctx.beginPath();

    ctx.arc(
        px,
        pz,
        5,
        0,
        Math.PI*2
    );

    ctx.fill();


    /*
       Police
    */

    ctx.fillStyle =
        "#ef4444";


    for(
        const car of police
    ) {

        const x =
            (car.x+260) /
            520 *
            w;

        const z =
            (car.z+260) /
            520 *
            h;


        ctx.beginPath();

        ctx.arc(
            x,
            z,
            3,
            0,
            Math.PI*2
        );

        ctx.fill();

    }

}


/* =========================================
   MESSAGE
========================================= */

let messageTimer = null;

function showMessage(text) {

    const element =
        document.getElementById(
            "message"
        );


    element.innerText = text;

    element.style.opacity = "1";


    clearTimeout(
        messageTimer
    );


    messageTimer =
        setTimeout(
            () => {

                element.style.opacity =
                    "0";

            },
            2400
        );

}


/* =========================================
   GAME OVER
========================================= */

function endGame() {

    gameOver = true;

    document.getElementById(
        "gameOver"
    ).style.display = "flex";

}


/* =========================================
   START
========================================= */

function startGame() {

    document.getElementById(
        "startScreen"
    ).style.display = "none";


    running = true;

    lastTime =
        performance.now();


    showMessage(
        "🌆 Chào mừng đến Open City!"
    );


    requestAnimationFrame(
        gameLoop
    );

}


/* =========================================
   LOOP
========================================= */

function gameLoop(time) {

    if(!running) return;


    requestAnimationFrame(
        gameLoop
    );


    const delta =
        Math.min(
            .05,
            (time-lastTime)/1000
        );


    lastTime = time;


    updatePlayer(delta);

    updateNPCs(delta);

    updatePolice(delta);

    updateMission(delta);

    updateWanted(delta);

    updateCamera();

    updateUI();


    /*
       Animate lamps
    */

    const pulse =
        1 +
        Math.sin(time*.004) *
        .08;


    for(
        const lamp of lamps
    ) {

        lamp.scale.set(
            pulse,
            pulse,
            pulse
        );

    }


    renderer.render(
        scene,
        camera
    );

}


/* =========================================
   RESIZE
========================================= */

function resize() {

    if(!camera || !renderer) return;


    camera.aspect =
        window.innerWidth /
        window.innerHeight;


    camera.updateProjectionMatrix();


    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

}


/* =========================================
   UTILITIES
========================================= */

function random(min,max) {

    return Math.random() *
        (max-min) +
        min;

}


function randomColor() {

    const colors = [
        0xef4444,
        0x3b82f6,
        0xeab308,
        0xa855f7,
        0xf97316,
        0x14b8a6,
        0xec4899
    ];


    return colors[
        Math.floor(
            Math.random() *
            colors.length
        )
    ];

}


/* =========================================
   BEGIN
========================================= */

loadThree();

</script>

</body>
</html>
"""

components.html(
    HTML,
    height=900,
    scrolling=False
)
