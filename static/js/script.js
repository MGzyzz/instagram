// animate input
document.querySelectorAll('.animate-input').forEach(e => {
    let input = e.querySelector('input')
    let button = e.querySelector('button')

    input.onkeyup = () => {
        if (input.value.trim().length > 0) {
            e.classList.add('active')
        } else {
            e.classList.remove('active')
        }

        if (checkSigninInput()) {
            signin_btn.removeAttribute('disabled')
        } else {
            signin_btn.setAttribute('disabled', 'true')
        }
    }

    if (button) {
        button.onclick = () => {
            if (input.getAttribute('type') === 'text') {
                input.setAttribute('type', 'password')
                button.innerHTML = 'Show'
            } else {
                input.setAttribute('type', 'text')
                button.innerHTML = 'Hide'
            }
        }
    }
})

checkSigninInput = () => {
    let inputs = signin_form.querySelectorAll('input')
    return Array.from(inputs).every(input => {
        return input.value.trim().length >= 6
    })
}

    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
$(".like-unlike-button").click(function() {
    var publicationId = $(this).data("publication-id");
    var likeUnlikeButton = $(this);
    var isLiked = likeUnlikeButton.hasClass("text-danger");
    if (isLiked) {
        $.ajax({
            url: `/api/publications/${publicationId}/unlike/`,
            method: "DELETE",
            headers: {
                'X-CSRFToken': csrfToken
            },

            success: function(data) {
                var likesCountElement = $("#likes-container-" + publicationId);
            likesCountElement.text(data.likes_count + ' отметок "Нравится"');
            likeUnlikeButton.removeClass("text-danger");
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(xhr.responseText);
            }
        });
    } else {
        $.ajax({
            url: `/api/publications/${publicationId}/like/`,
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken
            },

            success: function(data) {
                var likesCountElement = $("#likes-container-" + publicationId);
            likesCountElement.text(data.likes_count + ' отметок "Нравится"');
            likeUnlikeButton.addClass("text-danger");

            },
            error: function(xhr, textStatus, errorThrown) {
                console.log(xhr.responseText);
            }
        });
    }
    if (isLiked) {
        likeUnlikeButton.removeClass("text-danger");
    } else {
        likeUnlikeButton.addClass("text-danger");
    }
});
