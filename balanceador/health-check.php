<?php
// balanceador/health-check.php - Responsabilidade: Verificar se servidores estão vivos
// Atualiza o campo 'ativo' de cada servidor globalmente

global $servidores;

foreach ($servidores as &$servidor) {
    $conexao = @fsockopen($servidor['host'], $servidor['porta'], $errno, $errstr, 2);
    if ($conexao) {
        $servidor['ativo'] = true;
        fclose($conexao);
    } else {
        $servidor['ativo'] = false;
    }
}