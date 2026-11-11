<?php
// balanceador/servers.php - Responsabilidade: Configuração dos servidores
// Define quem são os servidores que o balanceador vai distribuir o tráfego

$servidores = [
    ['id' => 1, 'host' => 'shopnow-server1', 'porta' => 3002, 'ativo' => true, 'requisicoes' => 0],
    ['id' => 2, 'host' => 'shopnow-server2', 'porta' => 3003, 'ativo' => true, 'requisicoes' => 0],
    ['id' => 3, 'host' => 'shopnow-server3', 'porta' => 3004, 'ativo' => true, 'requisicoes' => 0],
];