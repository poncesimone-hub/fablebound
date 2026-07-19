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
        antialias: false,
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
let tiros_raio = 30;
let podePularDuplo = true;
let emAr = false;
let velocidadeBase = 5;
let ultimo_tiro = 0;
let scene_global = null;
let graphics = null;

function preload() {}

function create() {
    const scene = this;
    scene_global = this;
    
    // Fundo simples
    this.add.rectangle(640, 360, 1280, 720).setFill(0x87CEEB);
    
    // Chão
    const chao = this.add.rectangle(640, 700, 1280, 40).setFill(0x228B22);
    this.physics.add.existing(chao);
    chao.body.setImmovable(true);
    
    // Laura (personagem)
    laura = this.add.rectangle(640, 600, 40, 60, 0xC80000);
    this.physics.add.existing(laura);
    laura.body.setBounce(0.2);
    laura.body.setCollideWorldBounds(true);
    laura.body.setDrag(0.99);
    
    this.physics.add.collider(laura, chao, () => {
        emAr = false;
        podePularDuplo = true;
    });
    
    // Controles
    const keys = this.input.keyboard;
    keys.on('keydown-A', () => laura.body.setVelocityX(-velocidadeBase * 10));
    keys.on('keydown-D', () => laura.body.setVelocityX(velocidadeBase * 10));
    keys.on('keydown-SPACE', () => pular());
    keys.on('keydown-UP', () => atirar());
    keys.on('keydown-1', () => magiaAtual = 'raio');
    keys.on('keydown-2', () => magiaAtual = 'gelo');
    keys.on('keydown-3', () => magiaAtual = 'fogo');
    
    // Primeiro boss
    criarBoss(this, 'dragao', 200, 300);
    
    // UI Text
    this.uiText = this.add.text(10, 10, '', { fontSize: '14px', fill: '#fff', fontStyle: 'bold' });
}

function update() {
    if (!scene_global) return;
    
    // Remover tiros fora da tela
    tiros = tiros.filter(tiro => tiro.x < 1280);
    
    // Atualizar posição dos tiros
    tiros.forEach(tiro => {
        tiro.x += tiro.velocidade;
    });
    
    // Movimento dos bosses
    bosses.forEach((boss) => {
        boss.x += boss.vx;
        if (boss.x <= 0 || boss.x + 60 >= 1280) {
            boss.vx = -boss.vx;
        }
    });
    
    // Colisão tiros com bosses
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
    
    // Atualizar UI
    let uiTexto = `HP: ${Math.max(0, hp)}/${hpMax} | Moedas: ${moedas}\n`;
    uiTexto += `Magia: ${magiaAtual.toUpperCase()} | Tiros: ${tiros_raio}\n`;
    if (bosses.length > 0) {
        uiTexto += `Boss: ${bosses[0].nome} HP: ${Math.max(0, bosses[0].hp)}/${bosses[0].hp_max}`;
    }
    scene_global.uiText.setText(uiTexto);
    
    // Desenhar elementos
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
    } else if (magiaAtual === 'gelo' && tiros_raio > 5) {
        tiros.push({
            x: laura.x + 30,
            y: laura.y,
            velocidade: 6,
            dano: 8,
            tipo: 'gelo',
            color: 0xADD8E6
        });
    } else if (magiaAtual === 'fogo' && tiros_raio > 10) {
        tiros.push({
            x: laura.x + 30,
            y: laura.y,
            velocidade: 7,
            dano: 12,
            tipo: 'fogo',
            color: 0xFFA500
        });
    }
}

function criarBoss(scene, tipo, x, y) {
    const bosses_info = {
        dragao: { nome: 'Dragao', hp: 100, dano: 15, recompensa: 5 },
        cavaleiro: { nome: 'Cavaleiro', hp: 80, dano: 12, recompensa: 4 },
        mago: { nome: 'Mago', hp: 70, dano: 18, recompensa: 5 },
    };
    
    const info = bosses_info[tipo] || bosses_info.dragao;
    
    bosses.push({
        x: x,
        y: y,
        vx: 2,
        nome: info.nome,
        hp: info.hp,
        hp_max: info.hp,
        dano: info.dano,
        recompensa_moedas: info.recompensa
    });
}

function desenharElementos(scene) {
    // Limpar graphics antigos
    if (graphics) {
        graphics.destroy();
    }
    
    graphics = scene.make.graphics({ x: 0, y: 0, add: true });
    
    // Desenhar tiros (simples)
    tiros.forEach(tiro => {
        graphics.fillStyle(tiro.color, 1);
        graphics.fillCircle(tiro.x, tiro.y, 4);
    });
    
    // Desenhar bosses
    bosses.forEach(boss => {
        // Corpo do boss
        graphics.fillStyle(0x800000, 1);
        graphics.fillRect(boss.x - 25, boss.y - 35, 50, 70);
        
        // Barra de HP
        graphics.fillStyle(0x333333, 1);
        graphics.fillRect(boss.x - 25, boss.y - 45, 50, 4);
        
        graphics.fillStyle(0x00FF00, 1);
        const hp_percent = Math.max(0, boss.hp / boss.hp_max);
        graphics.fillRect(boss.x - 25, boss.y - 45, 50 * hp_percent, 4);
    });
}
