import { Routes } from '@angular/router';
import { LoginComponent } from './pages/authentication/login/login.component';

export const routes: Routes = [
    {
        path: "login",
        component: LoginComponent
    },
    {
        path: "menu",
        loadChildren: () => import('./pages/business/menu.routes').then((c) => c.MENU_ROUTES)
    },
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    }
];
