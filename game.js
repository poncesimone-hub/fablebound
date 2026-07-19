const config = {
    type: Phaser.AUTO,
    width: 1280,
    height: 720,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 300 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    parent: 'game',
    render: {
        pixelArt: true,
        antialiasGL: false
    }
};

const game = new Phaser.Game(config);

let laura;
let tiros = [];
let bosses = [];
let moedas = 0;
let hp = 100;
let hpMax = 100;
let magiaAtual = 'raio';
let barra_especial = 0;
let tiros_raio = 30;
let tiros_gelo = 0;
let tiros_fogo = 0;
let podePularDuplo = true;
let emAr = false;
let velocidadeBase = 5;
let ultimo_tiro = 0;
let scene_global = null;

function preload() {}

function create() {
    const scene = this;
    scene_global = this;
    
    this.add.rectangle(640, 360, 1280, 720).setFill(0x87CEEB);
    
    const chao = this.add.rectangle(640, 700, 1280, 40).setFill(0x228B22);
    this.physics.add.existing(chao);
    chao.body.setImmovable(true);
    
    laura = this.add.rectangle(640, 600, 40, 60, 0xC80000);
    this.physics.add.existing(laura);
    laura.body.setBounce(0.2);
    laura.body.setCollideWorldBounds(true);
    laura.body.setDrag(0.99);
    
    this.add.circle(640, 575, 8, 0xFFC896);
    
    this.add.line(640, 600, 0, 0, 30, 0, 0x000000).setStrokeStyle(3);
    this.add.circle(670, 600, 4, 0xFFFFFF);
    
    this.physics.add.collider(laura, chao, () => {
        emAr = false;
        podePularDuplo = true;
    });
    
    const keys = this.input.keyboard;
    keys.on('keydown-A', () => laura.body.setVelocityX(-velocidadeBase * 10));
    keys.on('keydown-D', () => laura.body.setVelocityX(velocidadeBase * 10));
    keys.on('keydown-SPACE', () => pular());
    keys.on('keydown-UP', () => atirar());
    keys.on('keydown-1', () => magiaAtual = 'raio');
    keys.on('keydown-2', () => magiaAtual = 'gelo');
    keys.on('keydown-3', () => magiaAtual = 'fogo');
    
    criarBoss(this, 'dragao', 200, 300);
    
    this.uiText = this.add.text(10, 10, '', { fontSize: '16px', fill: '#fff', fontStyle: 'bold' });
}

function update() {
    if (!scene_global) return;
    
    tiros = tiros.filter(tiro => tiro.x < 1280);
    tiros.forEach(tiro => {
        tiro.x += tiro.velocidade;
    });
    
    bosses.forEach((boss, idx) => {
        boss.x += boss.vx;
        if (boss.x <= 0 || boss.x + 60 >= 1280) {
            boss.vx = -boss.vx;
        }
        
        boss.contador_ataque++;
        if (boss.contador_ataque >= boss.intervalo_ataque) {
            boss.contador_ataque = 0;
        }
    });
    
    tiros.forEach((tiro, tIdx) => {
        bosses.forEach((boss, bIdx) => {
            const dist = Phaser.Math.Distance.Between(tiro.x, tiro.y, boss.x, boss.y);
            if (dist < 50) {
                boss.hp -= tiro.dano;
                tiros.splice(tIdx, 1);
                
                if (boss.hp <= 0) {
                    moedas += boss.recompensa_moedas;
                    bosses.splice(bIdx, 1);
                    if (bosses.length === 0) {
                        criarBoss(scene_global, 'dragao', 200, 300);
                    }
                }
            }
        });
    });
    
    let uiTexto = `HP: ${Math.max(0, hp)}/${hpMax}\n`;
    uiTexto += `Moedas: ${moedas}\n`;
    uiTexto += `Magia: ${magiaAtual.toUpperCase()}\n`;
    uiTexto += `Raio: ${tiros_raio} | Gelo: ${tiros_gelo} | Fogo: ${tiros_fogo}\n`;
    uiTexto += `Especial: ${Math.floor(barra_especial)}%\n`;
    if (bosses.length > 0) {
        uiTexto += `Boss: ${bosses[0].nome} (HP: ${bosses[0].hp}/${bosses[0].hp_max})`;
    }
    
    scene_global.uiText.setText(uiTexto);
    
    desenharElementos(scene_global);
}

function pular() {
    if (!emAr && laura) {
        laura.body.setVelocityY(-200);
        emAr = true;
    } else if (podePularDuplo && laura) {
        laura.body.setVelocityY(-200);
        podePularDuplo = false;
    }
}

function atirar() {
    const agora = Date.now();
    if (agora - ultimo_tiro < 100) return;
    ultimo_tiro = agora;
    
    if (magiaAtual === 'raio' && tiros_raio > 0) {
        tiros_raio--;
        tiros.push({
            x: laura.x + 30,
            y: laura.y,
            velocidade: 8,
            dano: 10,
            tipo: 'raio',
            color: 0xFFD700
        });
        barra_especial = Math.min(100, barra_especial + (100/30));
    } else if (magiaAtual === 'gelo' && tiros_gelo > 0) {
        tiros_gelo--;
        tiros.push({
            x: laura.x + 30,
            y: laura.y,
            velocidade: 6,
            dano: 8,
            tipo: 'gelo',
            color: 0xADD8E6
        });
        barra_especial = Math.min(100, barra_especial + (100/30));
    } else if (magiaAtual === 'fogo' && tiros_fogo > 0) {
        tiros_fogo--;
        tiros.push({
            x: laura.x + 30,
            y: laura.y,
            velocidade: 7,
            dano: 12,
            tipo: 'fogo',
            color: 0xFFA500
        });
        barra_especial = Math.min(100, barra_especial + (100/30));
    }
}

function criarBoss(scene, tipo, x, y) {
    const bosses_info = {
        dragao: { nome: 'Dragao', hp: 150, dano: 15, intervalo: 60, recompensa: 5 },
        cavaleiro: { nome: 'Cavaleiro', hp: 120, dano: 12, intervalo: 50, recompensa: 4 },
        mago: { nome: 'Mago', hp: 100, dano: 18, intervalo: 45, recompensa: 5 },
    };
    
    const info = bosses_info[tipo];
    if (!info) return;
    
    bosses.push({
        x: x,
        y: y,
        vx: 2,
        nome: info.nome,
        hp: info.hp,
        hp_max: info.hp,
        dano: info.dano,
        intervalo_ataque: info.intervalo,
        recompensa_moedas: info.recompensa,
        contador_ataque: 0
    });
}

function desenharElementos(scene) {
    // Remover graphics antigos
    scene.children.list = scene.children.list.filter(child => child.type !== 'Graphics');
    
    const graphics = scene.make.graphics({ x: 0, y: 0, add: false });
    
    // Desenhar tiros
    tiros.forEach(tiro => {
        graphics.fillStyle(tiro.color, 1);
        graphics.fillCircle(tiro.x, tiro.y, 5);
    });
    
    // Desenhar bosses
    bosses.forEach(boss => {
        graphics.fillStyle(0x800000, 1);
        graphics.fillRect(boss.x - 30, boss.y - 40, 60, 80);
        
        // Barra de HP
        graphics.fillStyle(0x333333, 1);
        graphics.fillRect(boss.x - 30, boss.y - 50, 60, 5);
        graphics.fillStyle(0xFF0000, 1);
        const hp_percent = boss.hp / boss.hp_max;
        graphics.fillRect(boss.x - 30, boss.y - 50, 60 * hp_percent, 5);
    });
    
    graphics.generateTexture('elementos', 1280, 720);
    scene.add.image(640, 360, 'elementos');
}
