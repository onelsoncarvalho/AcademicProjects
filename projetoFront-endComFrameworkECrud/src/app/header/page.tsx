"use client";
import React from 'react'
import Image from 'next/image';
import Link from 'next/link'
import { FiLogOut } from 'react-icons/fi'

import { useSession, signIn, signOut } from 'next-auth/react'
import BtSingInGoogle from '@/components/BtSingInGoogle';


export default function Header() {

  const { data: session, status } = useSession()

  return (
    <>
      <div className='flex justify-between max-w-[800px] mx-auto py-[20px] px-[10px]'>
        <Link href="/" className="pointer">
          <Image
            src="/Tasks.svg"
            width={100}
            height={100}
            className=""
            alt="logo" />
        </Link>
        <div className='flex gap-2'>

          {session?.user && (
            <Link href="/todo">
              <button className="bg-transparent border hover:bg-[#24292F]/90 focus:ring-4 focus:outline-none focus:ring-[#24292F]/50 font-medium rounded-xl text-sm px-5 py-3 text-center inline-flex items-center dark:focus:ring-gray-900 dark:hover:bg-[#24292f] mr-2 mb-2" type="button">Acessar Tarefas
              </button></Link>
          )}

          {status === 'loading' ? (
            <></>
          ) : session ? (
            <button type="button" onClick={() => signOut()} className="bg-transparent font-medium rounded-xl text-sm text-center inline-flex items-center">
              <img 
              className='w-10 mr-2 rounded-full' 
              src={`${session?.user?.image}`} 
              alt="Foto Perfil" />
              <h2>{session?.user?.name}</h2> <FiLogOut className='ml-2 text-[20px] text-[#24292f]' />
            </button>

          ) : (
            <BtSingInGoogle/>
          )}
        </div>
      </div>
    </>

  )
}


