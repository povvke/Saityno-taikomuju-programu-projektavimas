<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';

	let { children } = $props();
	let open = $state(false);

	function toggle(e: MouseEvent) {
		e.stopPropagation();
		open = !open;
	}

	function stop(e: Event) {
		e.stopPropagation();
	}

	function close() {
		open = false;
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape') close();
	}

	onMount(() => {
		if (typeof window === 'undefined') return;

		window.addEventListener('click', close);
		window.addEventListener('keydown', onKey);

		onDestroy(() => {
			window.removeEventListener('click', close);
			window.removeEventListener('keydown', onKey);
		});
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="navbar bg-base-200 px-4 shadow">
	<div class="flex-1">
		<a href="/" class="btn btn-ghost text-lg font-semibold">Home</a>
		<a href="/categories" class="btn btn-ghost">Categories</a>
	</div>

	<div class="flex-none">
		<div class="dropdown dropdown-end" class:dropdown-open={open}>
			Guest
			<button
				aria-label="login"
				aria-haspopup="true"
				aria-expanded={open}
				class="btn btn-ghost btn-circle avatar"
				onclick={toggle}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-8 h-8"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
					/>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M4.5 20.25a8.25 8.25 0 1115 0v.75H4.5v-.75z"
					/>
				</svg>
			</button>

			<div
				class="menu dropdown-content mt-3 p-4 shadow bg-base-100 rounded-box w-72 space-y-3"
				role="menu"
				tabindex="0"
				onclick={stop}
				onkeydown={(e) => e.key === 'Escape' && close()}
			>
				<form method="POST" action="/login" class="flex flex-col space-y-2" onsubmit={close}>
					<input
						type="email"
						name="email"
						placeholder="Email"
						class="input input-bordered w-full"
						required
					/>
					<input
						type="password"
						name="password"
						placeholder="Password"
						class="input input-bordered w-full"
						required
					/>
					<button class="btn btn-primary w-full" type="submit">Login</button>
				</form>

				<div class="divider my-0"></div>

				<a href="/register" class="btn btn-outline w-full">Register</a>
			</div>
		</div>
	</div>
</header>

{@render children?.()}
