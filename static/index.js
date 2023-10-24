function copyCommand(textToCopy, element) {
    const textArea = document.createElement('textarea');
    textArea.value = textToCopy;
    document.body.appendChild(textArea);

    textArea.select();

    document.execCommand('copy');

    document.body.removeChild(textArea);

    if (document.queryCommandSupported('copy')) {
        // console.log('Copied')
        let command = ""
        let target = $(element)
        // console.log(target)
        // console.log(target.attr("class"))

        command = target.find('span.command').text()
        target.find('span.command').text('Copied!')

        setTimeout(() => {
            target.find('span.command').text(command)
        }, 500)
    } else {
        // console.log('Oops, unable to copy');
    }
}
