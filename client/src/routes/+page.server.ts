import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';

export const load: PageServerLoad = async ({ fetch }) => {
	const res = await fetch(`${env.API_URL}/recipes`);
	const recipes = await res.json();
	return {
		recipes
	};
};
