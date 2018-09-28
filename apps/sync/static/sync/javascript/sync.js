$(document).ready(function () {
    $('#shop').on('click', function () {
        $('#shopMenu').toggle(400, "swing")
        $('#recipeMenu').hide(400, "swing")
        $('#profileMenu').hide(400, "swing")
    })

    $('#recipe').on('click', function () {
        $('#recipeMenu').toggle(400, "swing")
        $('#shopMenu').hide(400, "swing")
        $('#profileMenu').hide(400, "swing")
    })

    $('#profile').on('click', function () {
        $('#profileMenu').toggle(400, "swing")
        $('#shopMenu').hide(400, "swing")
        $('#recipeMenu').hide(400, "swing")
    })

    $('.itemRemove').submit(function (e) {
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.dropdown').html(serverResponse)
            }
        })

    })

    $('#addItemSync').submit(function (e) {
        console.log('before ajax')
        e.preventDefault()
        $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: $(this).serialize(),
            success: function (serverResponse) {
                $('.dropdown').html(serverResponse)
            }
        })
    })

    $('#addSync').on('click', function () {
        $('#postModal').toggle()
    })

    $('#closeButtn').on('click', function () {
        $('#postModal').hide()
    })


    $('.recipePost').on('click', function (e) {
        e.preventDefault()
        $(this).parent().next().show()
    })

    $('.closeModalBtn').on('click', function () {
        $('.recipeBoxModal').hide()
    })

    $('#modalShow').on('click', function(){
        $('#passwordModal').show()
    })

    $('#passwordCLose').on('click', function(){
        $('#passwordModal').hide()
    })
})


