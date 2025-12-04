import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const res = await fetch(`${env.PUBLIC_API_URL}/categories/${params.id}/recipes`);
	const recipes = await res.json();
	return {
		recipes
	};
};
