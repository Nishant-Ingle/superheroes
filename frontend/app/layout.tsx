'use client';

import localFont from "next/font/local";
import "./globals.css";
import {useState} from "react";
import Teams from "@/app/teams/page";
import Superheroes from "@/app/superheroes/page";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function RootLayout() {
  const superheroes = 'superheroes';
  const teams = 'teams';
  const [activeTab, setActiveTab] = useState(superheroes);

  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased container`}>

        <ul className="nav nav-tabs row">
          <li className="nav-item col-auto">
            <a className={`nav-link ${activeTab === superheroes ? 'active' : ''}`} aria-current="page" href="#" onClick={() => setActiveTab(superheroes)}>Superheroes</a>
          </li>
          <li className="nav-item col-auto">
            <a className={`nav-link ${activeTab === teams ? 'active' : ''}`} aria-current="page" href="#" onClick={() => setActiveTab(teams)}>Teams</a>
          </li>
        </ul>

        <div>
          {activeTab === superheroes && (<Superheroes/>)}
          {activeTab === teams && (<Teams/>)}
        </div>

      </body>
    </html>
  );
}
