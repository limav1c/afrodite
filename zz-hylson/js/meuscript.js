$(function () {
    
    if (saida=true){
        //não exibir o produto
    }
    
    // obtém carrinho da sessão
    var carrinho = sessionStorage.getItem('carrinho');

    // carrinho ainda não foi criado?
    if (carrinho == null) {
        // cria o carrinho
        carrinho = '';
        // coloca ele vazio mesmo na sessão, mas agora ele existe :-)
        sessionStorage.setItem('carrinho','');        
    }

    // tem algo no carrinho? 
    if (carrinho.length > 0) {

        // conta quantos elementos tem
        var elementos = carrinho.split(",");

        // mostra esse número perto do carrinho
        $("#numero_carrinho").text(elementos.length);
    } else {
        $("#numero_carrinho").text("vazio");
    }

    // código do botão "colocar no carrinho"
    $(document).on("click", ".btn_adicionar", function () {
        
        // obtém o id do botão clicado
        var id_botao = $(this).attr("id");

        // pegar id depois do nome do botão; ex: btn_NNNN
        var id_produto = id_botao.substring(4);
        
        // adiciona o produto no carrinho
        if (carrinho.length > 0) {
            carrinho += ","
        }
        carrinho += id_produto;

        // atualiza o número na tela: conta quantos tem agora e coloca lá
        var elementos = carrinho.split(",");
        $("#numero_carrinho").text(elementos.length);

        sessionStorage.setItem('carrinho',carrinho); 
    });


});