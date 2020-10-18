$(function() {
    $slider = $('.slider')
    $current = 0;
    let update = false
    id = null
    //notification bar
    const msgbar = document.querySelector('#msg');
        //removes html tags from strings
    const removetag = (str) => {
        
        let strippedheader = str.slice(4, -5)
        //to remove span tag in header
        const ptn3=/(<\/span>)/i;
        let spanfound=ptn3.exec(strippedheader);
       
        if (spanfound)
        {
         strippedheader=strippedheader.slice(0,-7)   
        }
        return strippedheader
    }
    const findtitle = article => {
        const pattern1 = /(<h1>.+<\/h1>)/i;
        const pattern2 = /(<h1.+>.+<\/h1>)/i;
        // console.log('header', header)
        //match first header without styles
        let match1 = pattern1.exec(article.content);
        //match first header with styles
        let match2 = pattern2.exec(article.content)
        if (match1) {
            return removetag(match1[0])


        } else if (match2) {
            let styleptn = /(\sstyle=.+;\")/
            let styles = styleptn.exec(match2[0])

            let strippedheader2 = match2[0].replace(styles[0], '')
            return removetag(strippedheader2)
        }
        return
    }
    function findimage(article){
        const ptn=/(<img\s.+\/>)/i;
        let img=ptn.exec(article.content)
        if (img){
            return img[0]
        }
        else{
            return null;
        }

    }
    const showMsg = (msg, type) => {
        switch (type) {
            case 'error':
                msgbar.classList.remove('success-msg');
                msgbar.classList.add('error-msg');
                msgbar.innerHTML = msg;
                break;
            case 'success':
                msgbar.classList.remove('error-msg');
                msgbar.classList.add('success-msg');
                msgbar.innerHTML = msg;
                break;
            default:

                msgbar.innerHTML = '';
                break;

        }
    }
    $("#article").submit(function(e) {
        e.preventDefault()

        let payload = { content: tinyMCE.activeEditor.getContent() };
        const title = findtitle(payload)
        const img=findimage(payload)
        console.log(img)
        if (!title) {
            let error = 'Add a Header 1 element to be used as the title'
            showMsg(error, 'error')
            return
        }
        if(!img){
            let error="no image found";
            showMsg(error,'error');
            return
        }

        payload.title = title;
        payload.img=img
        !update ? (fetch('/blog/publish', {
                method: "POST",
                headers: { 'Content-Type': "application/json" },
                body: JSON.stringify(payload)
            }).then((resp) => resp.json()).then(data => showMsg(data.success, 'success')).catch(err => showMsg(err, 'error')))
            //update post
            :
            (fetch(`/blog/update/${id}`, {
                method: "POST",
                headers: { 'Content-Type': "application/json" },
                body: JSON.stringify(payload)
            }).then((resp) => resp.json()).then(data => showMsg(data.success, 'success')).catch(err => showMsg(err, 'error')))
        return false;
    })
    tinymce.init({

        selector: '#mytexteditor',
        width: "100%",
        height: 500,
        statubar: true,
        setup: function(editor) {
            editor.on('init', function(e) {
                let loc = window.location.pathname
                let pattern = /update/
                if (pattern.test(loc)) {
                    id = loc.slice(-1)
                    update = true;
                    fetch(`/blog/update/${id}`)
                        .then(res => res.json()).then(data => tinyMCE.activeEditor.setContent(data.content)).catch(e => showMsg(e,"error"))
                }
            });
        },
        /* plugin */
        plugins: [
            "advlist save autolink link autosave image tinydrive lists charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
            "save table directionality emoticons template paste"
        ],
        tinydrive_token_provider: '/auth/jwt',

        /* toolbar */
        toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons save",
        images_upload_url: '/blog/upload_image',
        image_uploadtab: true,
        // save_onsavecallback: handlesubmit,
        /* style */
        style_formats: [{
                title: "Headers",
                items: [
                    { title: "Header 1", format: "h1" },
                    { title: "Header 2", format: "h2" },
                    { title: "Header 3", format: "h3" },
                    { title: "Header 4", format: "h4" },
                    { title: "Header 5", format: "h5" },
                    { title: "Header 6", format: "h6" }
                ]
            },
            {
                title: "Inline",
                items: [
                    { title: "Bold", icon: "bold", format: "bold" },
                    { title: "Italic", icon: "italic", format: "italic" },
                    { title: "Underline", icon: "underline", format: "underline" },
                    { title: "Strikethrough", icon: "strikethrough", format: "strikethrough" },
                    { title: "Superscript", icon: "superscript", format: "superscript" },
                    { title: "Subscript", icon: "subscript", format: "subscript" },
                    { title: "Code", icon: "code", format: "code" }
                ]
            },
            {
                title: "Blocks",
                items: [
                    { title: "Paragraph", format: "p" },
                    { title: "Blockquote", format: "blockquote" },
                    { title: "Div", format: "div" },
                    { title: "Pre", format: "pre" }
                ]
            },
            {
                title: "Alignment",
                items: [
                    { title: "Left", icon: "alignleft", format: "alignleft" },
                    { title: "Center", icon: "aligncenter", format: "aligncenter" },
                    { title: "Right", icon: "alignright", format: "alignright" },
                    { title: "Justify", icon: "alignjustify", format: "alignjustify" }
                ]
            }
        ]
    });


    function prev($current, $slider) {
        if ($current <= 0) {
            $prev = 39;
        } else {
            $prev = $current - 1;

        }
        $current = $prev;
        $previous = $prev.toString();
        $img_link = 'url(/static/memes/' + $previous + '.jpeg)';
        $slider.css('background-image', $img_link);

        return $current;

    }

    function next($current, $slider) {
        if ($current >= 39) {
            $next = 0;
        } else {
            $next = $current + 1;
        }
        $current = $next;
        $nextimg = $next.toString();
        $img_link = 'url(/static/memes/' + $nextimg + '.jpeg)';
        $slider.css('background-image', $img_link);


        return $current;

    }
    $('.arrow-left').on('click', function() {
        $current = prev($current, $slider);


    });
    $('.arrow-right').on('click', function() {
        $current = next($current, $slider);
    });

});