
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: "/pluscart/",
        data: {
            prod_id:id  // Sending product ID as a query parameter
        },
        success:function(data){
            console.log("data =", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});


$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: "/minuscart/",
        data: {
            prod_id:id  // Sending product ID as a query parameter
        },
        success:function(data){
            console.log("data =", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/removecart/",
        data: {
            prod_id:id  // Sending product ID as a query parameter
        },
        success:function(data){
            console.log("data =", data);
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
        }
    });
});

$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    console.log("ali1");
    $.ajax({
        type: "GET",
        url:"/pluswishlist/",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("ali1");
            //alert(data.message)
            window.location.href = `http://127.0.0.1:8000/productdetail/${id}` 
        }
    }) 
})
    
$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url:"/minuswishlist/",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href=`http://127.0.0.1:8000/productdetail/${id}`
        }
    })
})