$(function () {

    $(document).on("click", "#btListar", function () {

        // chamada ao backend
        $.ajax({
            url: 'http://localhost:5000/retornar_produtos',
            method: 'GET',
            dataType: 'json', // os dados são recebidos no formato json
            success: listar_produtos, // chama a função listar para processar o resultado
            error: function () {
                alert("erro ao ler dados, verifique o backend");
            }
        });

        // função executada quando tudo dá certo
        function listar_produtos(retorno) {
            if (retorno.resultado == 'ok') {
                $('#corpoTabelaProdutos').empty();
                produtos = retorno.detalhes;
                // percorrer a lista de produtos retornadas; 
                for (var i in produtos) { //i vale a posição no vetor
                    lin = `<tr>
                           <td>${produtos[i].descricao}</td>
                           <td>${produtos[i].situacao}</td>
                           <td><img src="http://localhost:5000/get_image/${produtos[i].id}" height=100 width=100></td>
                           <td>${produtos[i].cor}</td>
                           <td>${produtos[i].saida}</td>
                           </tr>`;
                    // adiciona a linha no corpo da tabela
                    $('#corpoTabelaProdutos').append(lin);
                }
            } else {
                alert("erro no retorno: " + retorno.detalhes);
            }
        }

    });
});