$(function () {

    $(document).on("click", "#btIncluir", function () {

        var dados_foto = new FormData($('#meuform')[0]);

        $.ajax({
            url: 'http://localhost:5000/save_image',
            method: 'POST',
            //dataType: 'json',
            data: dados_foto, // dados serão enviados em formato normal, para upload da foto
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                alert("enviou a foto direitinho!");
                insereProdutoNoBanco();
            },
            error: function (data) {
                alert("deu ruim na foto");
            }
        });





        function insereProdutoNoBanco() {

            //pegar dados da tela
            descricao = $("#campoDescricao").val();
            situacao = $("#campoSituacao").val();
            cor = $("#campoCor").val();
            saida = $("#campoSaida").val();

            // C:\\fakepath\\olho.jpg"
            // esse fakepath vem de algum lugar da biblioteca utilizada
            // só conta a contrabarra uma vez, inicia do zero
            nome_imagem = $("#campoFoto").val().substr(12);

            // preparar dados no formato json
            var dados = JSON.stringify({ descricao: descricao, situacao: situacao, cor: cor, nome_imagem: nome_imagem, saida: saida });
            // fazer requisição para o back-end
            $.ajax({
                url: 'http://localhost:5000/incluir_produto',
                method: 'POST',
                dataType: 'json', // os dados são recebidos no formato json
                //contentType: 'application/json', // dados enviados em json
                data: dados, // estes são os dados enviados
                success: produto_incluido, // chama a função listar para processar o resultado
                error: erroAoIncluirProduto
            });
            function produto_incluido(retorno) {
                if (retorno.resultado == "ok") { // a operação deu certo?
                    // informar resultado de sucesso
                    alert("produto cadastrada com sucesso!");
                    $("#campoDescricao").val();
                    $("#campoSituacao").val();
                    $("#campoCor").val();
                    $("#campoSaida").val();
                } else {
                    // informar mensagem de erro
                    alert(retorno.resultado + ":" + retorno.detalhes);
                }
            }
            function erroAoIncluirProduto(retorno) {
                // informar mensagem de erro
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }

    });
});