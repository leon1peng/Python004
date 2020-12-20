$(function() {
    $('#reg').click(function() {
        console.log("reg")
        $.ajax({
            'method': 'GET',
            'url': '/reg',
            'dataType': 'json',
            success: function() {
                console.log('成功')
            }
        });
    })
})