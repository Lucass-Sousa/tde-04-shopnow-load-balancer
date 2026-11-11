<?php
// balanceador/index.php - Responsória: Orquestrar a escolha e redirecionar
// Este arquivo agora tem APENAS as responsabilidade de orquestrar

require __DIR__ . '/servers.php';
require __DIR__ . '/health-check.php';
require __DIR__ . '/algorithms.php';

// Health check: atualiza status dos servidores
health_check($servidores);

// Escolher algoritmo (por enquanto usamos Round-Robin como default)
// Para usar Random, basta mudar para: $selecionado = escolherRandom($servidores);
$selecionado = escolherRoundRobin($servidores);

// Redirecionar para o servidor escolhido
if ($selecionado) {
    $urlDestino = "http://{$selecionado['host']}:{$selecionado['porta']}";
    header("Location: $urlDestino");
    exit;
} else {
    http_response_code(503);
    echo "ShopNow - Todos os servidores indisponíveis no momento.";
}