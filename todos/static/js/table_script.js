document.addEventListener('DOMContentLoaded', function () {
    var areaSpan = document.getElementById('id_area');
    var tipoIrrigadorInput = document.getElementById('id_tipo_irrigador');
    var camposDinamicos = document.querySelectorAll('[id^="campo1_"]');

    document.getElementById('id_estufa').addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    var areaSelecionada = selectedOption.getAttribute('data-area');
    var fazendaSelecionada = selectedOption.getAttribute('data-fazenda');

    // Atualize a área exibida
    document.getElementById('id_area').innerText = areaSelecionada;
    document.getElementById('id_fazenda').innerText = fazendaSelecionada;

    atualizarCampos(camposDinamicos);
    });

    // Adiciona um ouvinte de evento para o campo de área
    areaSpan.addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    var areaSelecionada = selectedOption.getAttribute('data-area');
    
    // Atualize a área exibida
    document.getElementById('area_selecionada').innerText = areaSelecionada || "Nenhuma área selecionada";
    atualizarCampos(camposDinamicos);
    });

    // Adiciona um ouvinte de evento para o campo tipo_irrigador
    tipoIrrigadorInput.addEventListener('change', function () {
    atualizarCampos(camposDinamicos);
    });

    camposDinamicos.forEach(function (campo) {
    var indice = campo.id.split('_')[1];

    // Adiciona um ouvinte de evento para cada campo "dose_"
    var doseInput = document.getElementById('dose_' + indice);
    doseInput.addEventListener('input', function () {
        atualizarCampos(camposDinamicos);
    });
    });

    function atualizarCampos(camposDinamicos) {
    // Obtenha o valor da área
    var area = parseFloat(areaSpan.innerText.replace(',', '.')) || 0;
    var tipoIrrigador = tipoIrrigadorInput.value;

    if (tipoIrrigador === '1') {
        camposDinamicos.forEach(function (campo) {
        // Extraia o índice do ID (por exemplo, campo1_1, campo1_2, etc.)
        var indice = campo.id.split('_')[1];
        var dose = parseFloat(document.getElementById('dose_' + indice).value.replace(',', '.'));

        if(!dose){
            campo.value = ""; // limita para 2 casas decimais
            document.getElementById('campo2_' + indice).value = "";
            document.getElementById('anti_camara_' + indice).value = "";
            document.getElementById('previsto_' + indice).value = "";
        }else{
            if(document.getElementById('dose_' + indice).value){

            var valorCampo1 = (area * dose)/2; //exemplo de cálculo
            var valorCampo2 = (area * dose)/2;
            var previsto = area * dose;

            // Atualize os campos de entrada com os valores calculados
            /*campo.value = valorCampo1;
            document.getElementById('campo2_' + indice).value = valorCampo2;
            document.getElementById('anti_camara_' + indice).value = "-";
            document.getElementById('previsto_' + indice).value = previsto;*/

            campo.value = parseFloat(valorCampo1).toFixed(2); // limita para 2 casas decimais
            document.getElementById('campo2_' + indice).value = parseFloat(valorCampo2).toFixed(2);
            document.getElementById('anti_camara_' + indice).value = "-";
            
            var valorCampo1Num = parseFloat(valorCampo1.toFixed(2));
            var valorCampo2Num = parseFloat(valorCampo2.toFixed(2));
            document.getElementById('previsto_' + indice).value = (valorCampo1Num + valorCampo2Num).toFixed(2);

            }
        }
        
        });
    } else {
        camposDinamicos.forEach(function (campo) {
        // Extraia o índice do ID (por exemplo, campo1_1, campo1_2, etc.)
        var indice = campo.id.split('_')[1];
        var dose = parseFloat(document.getElementById('dose_' + indice).value.replace(',', '.'));
        if(!dose){
            campo.value = ""; // limita para 2 casas decimais
            document.getElementById('campo2_' + indice).value = "";
            document.getElementById('anti_camara_' + indice).value = "";
            document.getElementById('previsto_' + indice).value = "";
        }else{
            if(document.getElementById('dose_' + indice).value){
            var valorAntiCamara = area * dose;  // Exemplo de cálculo para anti_camara

            // Atualize o campo anti_camara com o valor calculado
            document.getElementById('anti_camara_' + indice).value = parseFloat(valorAntiCamara).toFixed(2);
            document.getElementById('previsto_' + indice).value = parseFloat(valorAntiCamara).toFixed(2);
            campo.value = '-';
            document.getElementById('campo2_' + indice).value = '-';

            }
        }
        });
    }
    }
});