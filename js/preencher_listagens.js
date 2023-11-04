$(function () {

    // código genérico para listagem de produtos
    function listar_generico_por_categoria(categ) {

        // 1) Pedir ao backend os produtos daquela categoria

        var rota = 'http://localhost:5000/listar_produtos_categoria/' + categ;
        var acao = $.ajax({
            url: rota,
            dataType: 'json', // Os dados são recebidos no formato JSON
        });

        // Se a chamada der certo
        acao.done(function (dados) {
            if (dados.resultado == 'ok') {

                // percorrer os resultados
                for (var p of dados.detalhes) {

                    // Monta o esquema de um produto
                    var template = `
                        <div class="product-card">
                        <div class="product-image">
                            <img src="${p.nome_imagem}" class="product-thumb" alt="">
                            <button class="card-btn btn_adicionar" id="btn_3">Adicionar ao carrinho</button>
                        </div>
                        <div class="product-info">
                            <h2 class="product-brand">${p.descricao}</h2>
                            <p class="product-short-description">Situação: ${p.situacao} (cor: ${p.cor})</p>
                        </div>
                        </div>`;

                    // Adiciona o template preenchido na div
                    $('#listagem').append(lin);
                }
            } else {
                alert("ERRO na busca pelos dados :-/");
            }
        });

        // Se a chamada der erro
        acao.fail(function () {
            alert("Ocorreu algum erro na chamada ajax");
        });
    }

});