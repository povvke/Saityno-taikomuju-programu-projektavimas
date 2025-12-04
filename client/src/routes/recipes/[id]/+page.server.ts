import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const res = await fetch(`${env.PUBLIC_API_URL}/recipes/${params.id}`);
	const recipe = await res.json();

	const res_comments = await fetch(`${env.PUBLIC_API_URL}/recipes/${params.id}/comments`);
	const comments = await res_comments.json();
	return {
		recipe,
		comments
	};
};
