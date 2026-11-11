<?php
// balanceador/algorithms.php - Responsabilidade: Implementar os 2 algoritmos de escolha

// --- Função: Round-Robin ---
// Sequencial: 1 → 2 → 3 → 1 → 2 → 3 → ...
// Usa variável estática para manter o índice entre requisições
function escolherRoundRobin($servidores) {
    static $indiceRoundRobin = 0;
    $servidoresVivos = array_filter($servidores, fn($s) => $s['ativo']);
    if (count($servidoresVivos) > 0) {
        $alvo = $servidoresVivos[$indiceRoundRobin % count($servidoresVivos)];
        $indiceRoundRobin++;
        return $alvo;
    }
    return null;
}

// --- Função: Random ---
// Escolhe um servidor aleatório entre os vivos
function escolherRandom($servidores) {
    $servidoresVivos = array_filter($servidores, fn($s) => $s['ativo']);
    if (count($servidoresVivos) > 0) {
        $indiceAleatorio = array_rand($servidoresVivos);
        return $servidoresVivos[$indiceAleatorio];
    }
    return null;
}

