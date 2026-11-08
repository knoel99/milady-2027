import scene from "./scene.json" with { type: "json" };
import { mount } from "../runtime.js";

mount(scene, document.querySelector("#stage"));
