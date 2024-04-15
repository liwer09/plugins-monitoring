Write-Host "<<<ADFS_Decrypting>>>"
$fecha_actual = Get-Date
$certificado = Get-AdfsCertificate –CertificateType token-decrypting
$certificado_fecha = $certificado.Certificate.NotAfter


$diasRestantes = ($certificado_fecha - $fecha_actual).Days

if ($diasRestantes -le 30) {
    Write-Host "Critical - Quedan $diasRestantes para la caducidad del certificado"
    exit 2

}
elseif ($diasRestantes -le 90){
    Write-Host "Warning - Quedan $diasRestantes para la caducidad del certificado"
    exit 1
}
else {
    Write-Host "OK - Quedan $diasRestantes para la caducidad del certificado"
    exit 0
}