import React, { PropTypes, Component, useRef } from 'react'


export function FileSelect() {
    const inputFile = useRef(null);

    const onButtonClick = () => {
        // `current` points to the mounted file input element
        inputFile.current.click();
    };


    return (
        <div className="add-media">
            <button onClick={onButtonClick}>Open file upload window</button>
            <input type='file' id='file' ref={inputFile} style={{ display: 'none' }} />
        </div>
    )
}
