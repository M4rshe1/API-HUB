function copyCommand(textToCopy) {
    const textArea = document.createElement('textarea');
    textArea.value = textToCopy;

    document.body.appendChild(textArea);

    textArea.select();

    document.execCommand('copy');

    document.body.removeChild(textArea);

    if (document.queryCommandSupported('copy')) {
        // console.log('Copied')
        let command = ""
        let target = $(event.target)
        // console.log(target)
        // console.log(target.attr("class"))
        if (target.attr("class").includes('link')) {
            command = target.find('span.command').text()
            target.find('span.command').text('Copied!')
        } else {
            command = target.parent().find('span.command').text()
            target.parent().find('span.command').text('Copied!')
        }

        setTimeout(() => {
            if (target.attr("class").includes('link')) {
                target.find('span.command').text(command)
            }
            else {
                target.parent().find('span.command').text(command)
            }
        }, 2000)
    } else {
        // console.log('Oops, unable to copy');
    }
}
