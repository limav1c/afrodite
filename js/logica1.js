// Código de inicialização quando abrir a página do carrinho

// 1) Carregar a lista de IDs da sessão
var carrinho = sessionStorage.getItem('carrinho');

if (carrinho==null || carrinho.length === 0) {
  // Ou, redirecione para a página 'car_vazio':
  window.location.href = 'car_vazio.html';
}

// 2) Pedir ao backend a lista de todos os produtos
var rota = 'http://localhost:5000/listar_produtos'; // Certifique-se de definir a rota corretamente
var acao = $.ajax({
  url: rota,
  dataType: 'json', // Os dados são recebidos no formato JSON
});

// Se a chamada der certo
acao.done(function (dados) {
  if (dados.resultado == 'ok') {
    // 3) Fazer uma quebra da lista de IDs usando split (",")
    var partes = carrinho.split(',');

    // 4) Percorrer a lista de IDs
    for (var id_for of partes) {
      // 3.1) Para cada ID da lista, encontrar o produto na lista de produtos que recebeu do backend e exibir esse produto na página
      for (var p of dados.detalhes) {
        // O produto atual é igual ao produto que eu estou querendo mostrar?
        if (p.id == id_for) {
          // Monta a linha que vai mostrar o produto
          //var lin = '<div class="produto"> <img id="imagem" src="' + "C:\\Users\\maria\\Downloads\\kely\\kmelo\\testes-main\\afrodite\\imgs\"' + p.nome_imagem + '" title="foto carrinho" + p.nome_imagem"> <div class="info"> <p>' + p.descricao + '</p><p> SITUAÇÃO: SEMINOVO </p><p> VERDE </p><label class="checkbox"><input type="checkbox" id="checkbox" value=""></label></div></div><br>';

          var img = src=`<img id="imagem" src="${p.nome_imagem}" title="foto carrinho">`;
          var lin = img + ' <div class="info"> <p>' + p.descricao + '</p><p> SITUAÇÃO: SEMINOVO </p><label class="checkbox"><input type="checkbox" id="checkbox" value="" class="peca"></label></div></div><br>';
          //var lin = '<div class="produto"> <img id="imagem" src="C:\\Users\\maria\\Downloads\\kely\\kmelo\\testes-main\\afrodite\\imgs\"' + p.nome_imagem + '" title="foto carrinho"> <div class="info"> <p>' + p.descricao + '</p><p> SITUAÇÃO: SEMINOVO </p><p> VERDE </p><label class="checkbox"><input type="checkbox" id="checkbox" value=""></label></div></div><br>';

          
          // Adiciona a linha na div maior que abriga todas as linhas
          $('#listagem').append(lin);

          // Interrompe a busca porque já achou o produto
          break;
        }
      }
    }
  } else {
    alert("ERRO");
  }
});

// Se a chamada der erro
acao.fail(function () {
  alert("Ocorreu algum erro na chamada ajax");
});
