$(document).ready(function(){
    $('#add').submit(function (e) {
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.container').html(serverResponse)
            }
        })

    })
    
    $('.removeItem').submit(function (e) {
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.container').html(serverResponse)
            }
        })

    })

    $('#unCheck').submit(function (e) {
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.container').html(serverResponse)
            }
        })

    })

    $('#deleteItem').submit(function (e) { 
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.container').html(serverResponse)
            }
        })
    })
});

