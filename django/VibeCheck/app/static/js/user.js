$(document).ready(function(){

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }

    function fetchWithCSRF(url, options = {}) {
        const token = getCSRFToken();
        const headers = options.headers || {};
        headers['X-CSRFToken'] = token;
        options.headers = headers;
        options.credentials = 'same-origin';
        return fetch(url, options);
    }

    function handleMailboxButtons() {
        $(".new_request").off('click').on('click', function(e){
            e.preventDefault();
            e.stopPropagation();

            const button = $(this);

            if(button.prop('disabled')) return;
            button.prop('disabled', true);

            const form = button.closest("form");
            const formData = new FormData(form[0]);

            const actionValue = button.val() || button.attr('value');
            formData.set('action', actionValue);

            fetchWithCSRF("/ajax/mailbox-action/", {
                method: "POST",
                body: formData
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Server je vratio grešku: ' + res.status);
                }
                return res.json();
            })
            .then(json => {
                if(json.ok) {
                    const container = form.closest('.requests');
                    if(container.length) {
                        container.fadeOut(300, function() {
                            $(this).next('hr').remove();
                            $(this).remove();
                        });
                    } else {
                        form.fadeOut(300, function() {
                            $(this).next('hr').remove();
                            $(this).remove();
                        });
                    }
                    setTimeout(() => {
                        refreshFriends();
                        refreshCollabs();
                        refreshMessages();
                    }, 400);
                }
            })
            .catch(err => {
                console.error('GREŠKA:', err);
                button.prop('disabled', false);
                alert('Došlo je do greške: ' + err.message);
            });
        });
    }

    function refreshFriends() {
        fetchWithCSRF("/ajax/friends/")
            .then(res => res.text())
            .then(html => {
                const friendsList = document.querySelector(".friends-list");
                if(friendsList) {
                    friendsList.innerHTML = html;
                }
            })
            .catch(err => console.log('Greška pri učitavanju prijatelja:', err));
    }

    function refreshCollabs() {
        fetchWithCSRF("/ajax/collabs/")
            .then(res => res.text())
            .then(html => {
                const collabsList = document.querySelector(".collabs-list");
                if(collabsList) {
                    collabsList.innerHTML = html;
                }
            })
            .catch(err => console.log('Greška pri učitavanju collab-ova:', err));
    }

    function refreshMessages() {
        fetchWithCSRF("/ajax/messages/")
            .then(res => res.text())
            .then(html => {
                const mailList = document.querySelector(".mail-list");
                if(mailList) {
                    mailList.innerHTML = html;
                    handleMailboxButtons();
                }
            })
            .catch(err => console.log('Greška pri učitavanju poruka:', err));
    }

    $("#addfr").click(function(){
        let form = document.getElementById("addfriendform");
        if(form) {
            form.style.display = "block";
            document.getElementById("addfr").style.display = "none";
        }
    });

    $("#addfriend").click(function(){
        let form = document.getElementById("addfriendform");
        if(form) {
            form.style.display = "none";
            document.getElementById("addfr").style.display = "block";
        }
    });

    if(window.location.pathname === '/user/' || window.location.pathname === '/user') {
        setInterval(() => {
            refreshFriends();
            refreshCollabs();
            refreshMessages();
        }, 5000);
    }

    handleMailboxButtons();
});