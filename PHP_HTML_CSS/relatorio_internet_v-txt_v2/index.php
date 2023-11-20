<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>Monitoramento</title>
    <link rel="stylesheet" href="style.css">
</head>

<?php // Processo de todos o site
    // Varias Globais
    $_contato_lan = 0;
    $_contato_wan = 0;

    // Variaveis data/hora
    date_default_timezone_set('America/Sao_Paulo');
        $_data_atual_global = date('d/m/Y');
        $_dia_atual_global = date('d');
        $_mes_atual_global = date('m');
        $_ano_atual_global = date('Y');
        // horario
        $_hora_atual_global = date("H:i");
        $_valor_hora_global = date("H");
        $_valor_minu_global = date("i");
        $_valor_secu_global = date('s');

    // Variaveis de local arquivo
    $_local_arq_LAN = "_status_LAN.log";
    $_local_arq_WAN = "_status_WAN.log";

    // Corrigo o valor numerico que começa com "0". Quando o relogio muda o horário, tipo 14:02, o valor é dividido em "hora" e 
    // "minutos". Quando você coloca o minuto, por esta començando por "0" o PHP entende que é octdecimal.
    function _001_conver_oct_dec($_dados_OD) {
        $_001_convert_OD = str_pad($_dados_OD, 8, "0", STR_PAD_LEFT);
        return sprintf("%02d",$_001_convert_OD + 1);
        echo $_001_convert_OD;
    }  

    // Transformando os dados da LAN em array
    if (file_exists($_local_arq_LAN)) {
    $_valor_status_array_LAN = file_get_contents ($_local_arq_LAN);
    $_status_LAN = explode('-', $_valor_status_array_LAN);
    $_valor_data_LAN = $_status_LAN[0];
    $_valor_horario_LAN = $_status_LAN[1];
    $_valor_status_LAN = $_status_LAN[2];
    // quebrando a variavel $_valor_data
    $_valor_data_array_LAN = explode('/', $_valor_data_LAN);
    $_valor_dia_LAN = $_valor_data_array_LAN[0];
    $_valor_mes_LAN = $_valor_data_array_LAN[1];
    $_valor_ano_LAN = $_valor_data_array_LAN[2];
    // Quebrando a variavel $_valor_horario_LAN
    $_valor_hora_array_LAN = explode(':', $_valor_horario_LAN);
    $_valor_hora_LAN = $_valor_hora_array_LAN[0];
    $_valor_minu_LAN = _001_conver_oct_dec($_valor_hora_array_LAN[1]);
    $_valor_segu_LAN = _001_conver_oct_dec($_valor_hora_array_LAN[2]);
    } else {
        $_valor_status_LAN[2] = "DESCONHECIDO";
    }

    // Transformando os dados da WAN em array
    if (file_exists($_local_arq_WAN)) {
    $_valor_status_array_WAN = file_get_contents($_local_arq_WAN);
    $_status_WAN = explode("-", $_valor_status_array_WAN);
    $_valor_data_WAN = $_status_WAN[0];
    $_valor_horario_WAN = $_status_WAN[1];
    $_valor_status_WAN = $_status_WAN[2];
    // Quebrando a variavel $_valor_data_WAN
    $_valor_data_array_WAN = explode('/', $_valor_data_WAN);
    $_valor_dia_WAN = $_valor_data_array_WAN[0];
    $_valor_mes_WAN = $_valor_data_array_WAN[1];
    $_valor_ano_WAN = $_valor_data_array_WAN[2];
    // Quebrando a variavel $_valor_horario_WAN
    $_valor_hora_array_WAN = explode(':', $_valor_horario_WAN);
    $_valor_hora_WAN = $_valor_hora_array_WAN[0];
    $_valor_minu_WAN = _001_conver_oct_dec($_valor_hora_array_WAN[1]);
    $_valor_segu_WAN = _001_conver_oct_dec($_valor_hora_array_WAN[2]);
    }  else {
        $_valor_status_WAN[2] = "DESCONHECIDO";
    }

    

     //-------------------------------------------FUNÇÕES-------------------------------------------------------------------//
    function _002_condicoes_tempo_lan($_valor_LAN, $_valor_global) {        
        
    }
    function _003_condicoes_tempo_lan($_valor_WAN) {
    }

    $_valor_total_global = $_mes_atual_global.$_dia_atual_global.$_valor_hora_global.$_valor_minu_global;
    $_valor_total_LAN_log = $_valor_mes_LAN.$_valor_dia_LAN.$_valor_hora_LAN.$_valor_minu_LAN;
    $_valor_total_WAN_log = $_valor_mes_LAN.$_valor_dia_LAN.$_valor_hora_LAN.$_valor_minu_LAN;
?>
<!--img src="./img/img_003_ping_v2_alerta.jpg" alt="OFF"-->
<!--CORPO HTML-->
<body>    
<main>
    <!--Seção data-->
    <div class="div_data">
        <h1 class="h1_hora_certa">Hora Certa</h1>
        <h2 id="h2_data_div_data"><?=$_data_atual_global?></h2>
        <h3 id="h3_data_div_data"><?=$_hora_atual_global?></h3>        
    </div>

    <!--Seção LAN-->
    <div class="div_lan">
    <h2 id="h2_lan">Status da Rede Local (LAN)</h2>
    <?php
    if ($_valor_status_LAN == " ATIVO") {
        if ($_valor_total_LAN_log < $_valor_total_global) {
            echo '<img src="./img/img_003_ping_v2_neutro.jpg">';
        } else {
            echo '<img src="img/img_003_ping_v2_on.jpg">'; 
        }
    } elseif ($_valor_status_LAN == " INATIVO") {
        if ($_valor_total_WAN_log < $_valor_total_global) {
            echo '<img src="./img/img_003_ping_v2_neutro.jpg">';
        } else {
            echo '<img src="img/img_003_ping_v2_off.jpg">';
        }
    } else {
        echo '<img src="img/img_003_ping_v2_neutro.jpg">';
    }
    ?>
    </div>
    
    <!--Seção WAN-->
    <div class="div_wan">
    <h2 id="h2_wan"> Status da internet (WAN) </h2>
    <?php
        if ($_valor_status_WAN == " ATIVO") {            
            if ($_valor_total_WAN_log < $_valor_total_global) {
                echo '<img src="img/img_003_ping_v2_neutro.jpg">';
            } else {
                echo '<img src="img/img_003_ping_v2_on.jpg">';
            }
        } elseif ($_valor_status_WAN == " INATIVO") {  
            if ($_valor_total_WAN_log < $_valor_total_global) {
                echo '<img src="img/img_003_ping_v2_neutro.jpg">';
            }
            else {                    
                echo '<img src="img/img_003_ping_v2_off.jpg">';
            }             
        } else {
            echo '<img src="img/img_003_ping_v2_neutro.jpg">';
        }  
        ?>
    </div>
    <div class="rodape">
        Thiago Alves Pinheiro</br>
        <a href="th_grifon@hotmail.com" >th_grifon@mail.com</a></br>
        <a href="https://github.com/dev-drizzithiago" target="_blank"> dev-drizzithiago </a>
    </footer>
</main>

<!-- Teste para linhas de comando-->
    <div class="analise_desnv">
        <h3>Analise de informações<h3>
        <?="Analisando informações contidas na LAN: ==> "?>
        <?="$_valor_mes_LAN.$_valor_dia_LAN.$_valor_hora_WAN.$_valor_minu_LAN < 
        $_mes_atual_global.$_dia_atual_global.$_valor_hora_global.$_valor_minu_global"?> 
        <!--<?=print_r($_valor_hora_array_LAN)?>-->
        <?="</br>"?>
        <?="Analisando informações contidas na WAN: ==> "?>
        <?="$_valor_mes_WAN.$_valor_dia_WAN.$_valor_hora_WAN.$_valor_minu_WAN < 
        $_mes_atual_global.$_dia_atual_global.$_valor_hora_global.$_valor_minu_global"?> 
        <!--<?=print_r($_valor_hora_array_WAN)?>-->
    </div>
</body>
</html>