$(document).ready(function(){

    function getCSRFToken() {
        return $('meta[name="csrf-token"]').attr('content');
    }

    function fetchWithCSRF(url, options={}) {
        const token = getCSRFToken();
        options.headers = options.headers || {};
        options.headers['X-CSRFToken'] = token;
        options.credentials = 'same-origin';
        return fetch(url, options);
    }

    function refreshParticipants() {
        const collabId = document.body.dataset.collabId;
        if(!collabId) return;

        fetch(`/ajax/participants/${collabId}/`)
            .then(res => res.text())
            .then(html => $(".participants-list").html(html))
            .catch(err => console.log(err));
    }

   function refreshFriendsList() {
        const collabId = document.body.dataset.collabId;
        if(!collabId) return;


        fetch(`/ajax/friends-collab/${collabId}/`)
            .then(res => res.json())
            .then(data => {
                const list = $(".friends-list").empty();
                data.forEach(friend => {

                    const form = $(`
                        <form class="friend-invite-form">
                            <input type="hidden" name="form_type" value="friends">
                            <input type="hidden" name="friend_id" value="${friend.friend_id}">
                            ${friend.username}
                        </form>
                    `);

                    if(!friend.sent) {
                        const btn = $('<button type="button" class="btn addfriend">+</button>');
                        form.append(btn);
                    }

                    form.append('<br>');
                    list.append(form);
                });
            })
            .catch(err => console.log('Error:', err));
    }

   $(document).on('click', '.addfriend', function(e){
        e.preventDefault();
        e.stopPropagation();

        const button = $(this);

        if(button.prop('disabled')) {
            return;
        }
        button.prop('disabled', true);

        const form = button.closest('form')[0];

        if(!form) {
            button.prop('disabled', false);
            return;
        }

        const data = new FormData(form);
        const collabId = document.body.dataset.collabId;

        fetchWithCSRF(window.location.pathname, {
            method: "POST",
            body: data,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(res => {
                if(!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(resp => {
                if(resp.ok){
                    $('#error-message').hide();

                    refreshParticipants();
                    setTimeout(refreshFriendsList, 500);
                } else {
                    if(resp.error) {
                        $('#error-message').text(resp.error).fadeIn();
                    }
                    button.prop('disabled', false);
                }
            })
            .catch(err => {
                button.prop('disabled', false);
                alert('Greška: ' + err.message);
            });
   });

    setInterval(() => {
        refreshParticipants();
        refreshFriendsList();
    }, 5000);
    refreshParticipants();
    refreshFriendsList();
});