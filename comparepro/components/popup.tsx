import React, { useState, useEffect } from 'react';
import { MdCancel } from "react-icons/md";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';


/**
 * A popup that appears when the user has reached the maximum number of comparisons
 * allowed in the free version of the app.
 * @param {number} value The number of comparisons the user has made.
 */
export default function PopupCounter({ value }: { value: number|null }) {
    if (value === null) {
        return null
    }
    const [open, setOpen] = useState(value <= 0);
    
    useEffect(() => {
        // Attach an event listener to the compare button to open the popup
        // when the button is clicked
        const compare_button = document.querySelector('#compare-button');
        compare_button?.addEventListener('click', () => {
            if (value <= 0) {
                setOpen(true);
            }
        });
    }, []);

    /**
     * Close the popup when the user clicks the close button.
     */
    const closeModal = () => {
        setOpen(false);
    }
     
    return (
        <div className='flex flex-col items-center justify-center rounded-lg'>
            <Popup open={open} closeOnDocumentClick onClose={closeModal}
                modal nested className='bg-white p-2'>
                <div className='flex flex-col items-center justify-center bg-white p-6'>
                    <button onClick={closeModal}>
                        {/* Close button */}
                        <MdCancel size={25} className='absolute top-2 right-2 cursor-pointer'/>
                    </button>
                    <h1 className='text-xl mb-2'>Comparison Limit Reached</h1>
                    <p>You have reached the maximum number of comparisons allowed.</p>
                    <p>This is a Beta version. We will let you know when this limit is lifted.</p>
                </div>
            </Popup>
        </div>
    )
};
