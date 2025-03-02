import { Routes } from '@angular/router';
import { ListComponent } from './list/list.component';
import { DetailComponent } from './detail/detail.component';
import { CreateComponent } from './create/create.component';

export const MENU_ROUTES: Routes = [
    {
        path: 'list',
        component: ListComponent
    },
    {
        path: 'list/:id/details',
        component: DetailComponent
    },
    {
        path: 'create',
        component: CreateComponent
    },
    {
        path: '',
        redirectTo: 'list',
        pathMatch: 'full'
    }
];
