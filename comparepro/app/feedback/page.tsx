"use client"
import Link from 'next/link'
import ContactForm from "./feedback"
import { LiaCommentsSolid } from "react-icons/lia";

export default function Feedback() {
    return (
        <div className="flex flex-col justify-center h-auto min-h-screen w-full items-center py-8 bg-gradient-to-b from-white to-black via-gray-500">
            <div className='flex flex-col justify-center items-center mb-12 rounded-lg md:sm:w-1/2 lg:w-1/3 py-4 bg-white shadow'>
                <Link href="/" className='mt-4'>
                    <img src="/compareprologo.png" alt="ComparePro" className="h-8 ml-2 cursor-pointer mb-6"/>
                </Link>
                <div className='flex flex-col justify-center items-center border-b border-gray-300 mb-4 w-3/4'>
                    <h1 className="text-2xl m-4">Feedback Form</h1>
                    <LiaCommentsSolid className="text-blue-500 text-4xl mb-4" />
                    <p className="text-xs lg:md:text-sm mb-4">
                        We would love to hear your thoughts, suggestions, concerns or problems with anything so we can improve!
                    </p>         
                </div>
                <ContactForm />
            </div>
        </div>
    )
}