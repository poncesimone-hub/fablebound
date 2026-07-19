const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 200 },
            debug: false
        }
    },
    scene: {
        create: create,
        update: update
    },
    parent: 'game'
};

const game = new Phaser.Game(config);

let player;
let cursors;
let platforms;
let score = 0;
let scoreText;

function create() {
    // Fundo
    this.add.rectangle(400, 300, 800, 600).setFill(0x87CEEB);
    
    // Chão
    const ground = this.add.rectangle(400, 580, 800, 40).setFill(0x228B22);
    this.physics.add.existing(ground);
    ground.body.setImmovable(true);
    
    // Plataformas
    platforms = this.physics.add.staticGroup();
    platforms.create(400, 580, null).setScale(2).refreshBody();
    platforms.create(600, 400, null);
    platforms.create(50, 250, null);
    platforms.create(750, 220, null);
    
    // Jogador
    player = this.add.rectangle(100, 450, 32, 48, 0xC80000);
    this.physics.add.existing(player);
    player.body.setBounce(0.2);
    player.body.setCollideWorldBounds(true);
    
    // Colisão
    this.physics.add.collider(player, platforms);
    
    // UI
    scoreText = this.add.text(16, 16, `Score: ${score}`, { fontSize: '20px', fill: '#fff' });
    
    // Controles
    cursors = this.input.keyboard.createCursorKeys();
    this.input.keyboard.on('keydown-SPACE', () => {
        if (player.body.touching.down) {
            player.body.setVelocityY(-300);
        }
    });
}

function update() {
    if (cursors.left.isDown) {
        player.body.setVelocityX(-160);
    } else if (cursors.right.isDown) {
        player.body.setVelocityX(160);
    } else {
        player.body.setVelocityX(0);
    }
    
    scoreText.setText(`Score: ${score}`);
}
