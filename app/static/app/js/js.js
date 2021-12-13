$('.plus-cart').click(function(){
    var id=$(this).attr('pid').toString();
    console.log(id);
    var eml=this.parentNode.children[2];
    console.log(eml);
    $.ajax({
        type:'GET',
        url:'/plus_cart',
        data: {
            prod_id: id
        },
        success:function(data){
            eml.innerText=data.quantity
           document.getElementById('amount').innerText = data.amount
           document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr('pid').toString();
    console.log(id)
    var eml=this.parentNode.children[2]
    $.ajax({
        type:'GET',
        url:'/minus_cart',
        data: {
            prod_id: id
        },
        success:function(data){
            eml.innerText=data.quantity
           document.getElementById('amount').innerText = data.amount
           document.getElementById('totalamount').innerText = data.totalamount
           
        }
    })
})

$('.remove').click(function(){
    var id=$(this).attr('pid').toString();
    console.log(id)
    var eml=this
    $.ajax({
        type:'GET',
        url:'/remove_cart',
        data: {
            prod_id: id
        },
        success:function(data){
            console.log("Delete")
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            
        }
    })
})