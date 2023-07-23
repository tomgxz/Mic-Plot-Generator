function sendServerData(mic,scene,actor,speaking) {
    $.ajax({
        url: `${$('meta[name="act-id"]').attr('content')}/update/${mic}/${scene}`,
        //dataType: "json",
        type: "POST",
        async: true,
        data: {
            csrfmiddlewaretoken: $('meta[name="csrf-token"]').attr('content'),
            mic:mic,
            scene:scene,
            actor:actor,
            speaking:speaking
        },
        success: function (data) {
           console.log("Saved successfully")
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status == 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status == 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }

            console.warn(msg)

            alert("Error whilst saving, reverting changes.")
        }
    })
}

window.onload = async () => {
    $.ajaxSetup({
        headers: {
            'X-CSRF-Token': $('meta[name="csrf-token"]').attr('content')
        }
    });    

    var selectionActive = false

    $(".mic-plot-table .table-cell").on("click",(e) => {

        if (!($(e.currentTarget).hasClass("editable"))) return

        if (false) {
            
            var _ = $(e.currentTarget)
            
            if (_.hasClass("speaking")) {
                _.removeClass("speaking")
                _.addClass("nonspeaking")
            } else if (_.hasClass("nonspeaking")) {
                _.removeClass("nonspeaking")
            } else {
                _.addClass("speaking")
            }

        } else {
            var _basic = e.currentTarget.querySelector(".text-input-replace")
            var _ = $(_basic)

            if (_.html().includes("<input") || selectionActive) { return }
            
            var content = _.text()
            var width = getComputedStyle(e.currentTarget).width
            var id = _.attr("id")

            e.currentTarget.style.width = width
            _basic.style.width = width

            _.html(`<input type="text" class="text-input-replace-input" name="${id}" id="${id}" cols=1 value="${content}" style="width:${width}!important;padding:0!important"></input>`)

            inputElement = $(_basic.querySelector(`#${id}`))
            inputElement.focus()

            var resetelement = function(){
                content = inputElement.val();
                _.html("")
                _.text(content)

                _basic.parentNode.style.width = ""
                
                if (content != "") _.parent("").addClass("speaking")
                else {
                    _.parent("").removeClass("speaking")
                    _.parent("").removeClass("nonspeaking")
                }

                var isspeaking = 0
                if (_.parent("").hasClass("nonspeaking")) isspeaking=1
                if (_.parent("").hasClass("speaking")) isspeaking=2

                console.log(isspeaking)
                
                sendServerData(_.attr("data-mic"),_.attr("data-scene"),content,isspeaking)
            }
            
            inputElement.on("blur",resetelement)
            inputElement.keypress((e) => {
                var keycode = (e.keyCode ? e.keyCode : e.which);
                if(keycode == '13') resetelement()
            })

        }

    })
}


// shows/show/1            /test           /act/1           /update/1            /1/
// shows/show/<int:show_id>/<str:show_name>/act/<int:act_id>/update/<int:mic_id>/<int:scene_id>